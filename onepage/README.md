# Werner Bau – Onepage Relaunch 2026

Quellcode der Vibe-Sections der Onepage-Site „wernerbau2026“ (https://wernerbau2026.onepage.me).

- `sections/<name>/` – React-Komponenten (index.tsx + styles.module.css) je Abschnittstyp:
  header, hero, services, about, content, gallery, certs, team, contact, footer
- `gen.py` – erzeugt die package.json (Controls + Standardwerte) je Abschnitt
- `pages.py` – Seitenaufbau und Inhalte je Seite (`python3 pages.py <seite>` schreibt nach `out/`)

Benötigt `uploaded.json` (Mapping Original-Bild-URL → Onepage-CDN-URL) neben den Skripten.

Seitenweit per Site-Einstellung „code_body“: schwebender Kontakt-Button (Anrufen / Anfrage senden / WhatsApp).
Die WhatsApp-Nummer wird dort in `WA_NUMBER` eingetragen; solange sie leer ist, bleibt der WhatsApp-Button ausgeblendet.
