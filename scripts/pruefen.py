#!/usr/bin/env python3
"""Prüft, ob die OKF-Dateien vollständig sind.

Aufruf (aus dem Repo-Ordner):   python scripts/pruefen.py

Geprüft wird für jede .md-Datei unter okf/:
  - Kopf (Frontmatter) zwischen --- vorhanden und lesbar
  - type, title, description gesetzt
  - bei concept/rule mit status active: sources, verified (mit human:), stale_after in der Zukunft
  - alle Links in eckigen Klammern zeigen auf existierende Dateien
  - jede Datei steht in der index.md ihres Ordners

Braucht nur Python 3. Kein pip install nötig: der Kopf wird mit einem
kleinen Mini-Parser gelesen, damit das Beispiel ohne Abhängigkeiten läuft.
"""
import datetime as dt
import re
import sys
from pathlib import Path

OKF = Path(__file__).resolve().parent.parent / "okf"
SKIP = {"log.md", "_vorlage.md"}
LINK = re.compile(r"\[[^\]]*\]\(([^)#]+)\)")


def lies_kopf(text):
    """Sehr kleiner YAML-Leser: reicht für flache Felder und die Listen hier."""
    if not text.startswith("---"):
        return None
    teile = text.split("---", 2)
    if len(teile) < 3:
        return None
    kopf = {}
    for zeile in teile[1].splitlines():
        if ":" in zeile and not zeile.startswith((" ", "-")):
            k, _, v = zeile.partition(":")
            kopf[k.strip()] = v.strip()
    kopf["_roh"] = teile[1]
    return kopf, teile[2]


def pruefe(datei):
    fehler = []
    text = datei.read_text(encoding="utf-8")
    ergebnis = lies_kopf(text)
    if ergebnis is None:
        return ["kein Kopf zwischen --- Linien"]
    kopf, body = ergebnis

    for feld in ("type", "title", "description"):
        if not kopf.get(feld) or kopf[feld].startswith("<"):
            fehler.append(f"Feld fehlt oder ist noch Platzhalter: {feld}")

    typ = kopf.get("type")
    status = kopf.get("status", "active")
    if typ in ("concept", "rule") and status != "draft":
        if "sources:" not in kopf["_roh"] or "resource:" not in kopf["_roh"]:
            fehler.append("sources fehlt (woher kommt die Definition?)")
        if "human:" not in kopf["_roh"]:
            fehler.append("verified hat keinen human:-Eintrag (wer hat geprüft?)")
        sa = kopf.get("stale_after", "")
        try:
            if dt.date.fromisoformat(sa) < dt.date.today():
                fehler.append(f"stale_after ist abgelaufen: {sa}")
        except ValueError:
            fehler.append(f"stale_after fehlt oder ist kein Datum: {sa!r}")
        if "Nicht gemeint" not in body:
            fehler.append("kein Satz 'Nicht gemeint:' (die Abgrenzung fehlt)")

    for ziel in LINK.findall(body):
        if ziel.startswith("http"):
            continue
        if not (datei.parent / ziel).resolve().exists():
            fehler.append(f"Link zeigt ins Leere: {ziel}")

    if datei.name != "index.md":
        index = datei.parent / "index.md"
        if not index.exists():
            fehler.append("Ordner hat keine index.md")
        elif datei.name not in index.read_text(encoding="utf-8"):
            fehler.append(f"steht nicht in {index.relative_to(OKF.parent)}")
    return fehler


def main():
    dateien = sorted(p for p in OKF.rglob("*.md") if p.name not in SKIP)
    gesamt = 0
    for d in dateien:
        for f in pruefe(d):
            print(f"FEHLER  {d.relative_to(OKF.parent)}: {f}")
            gesamt += 1
    print(f"\n{len(dateien)} Dateien geprüft, {gesamt} Fehler")
    sys.exit(1 if gesamt else 0)


if __name__ == "__main__":
    main()
