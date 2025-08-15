# Bereitstellung von Metadaten
Für die Bereitstellung von Metadaten können beliebige Quellen verwendet werden.
Ein unterstütztes Exportformat sind RSS/XML-Feeds in Übereinstimmung mit den [Spezifikationen](../README.md).

## Excel Editor
Eine Metadaten-Editor-Vorlage für Microsoft Office kann zur Erfassung und zum Export von Metadaten verwendet werden.

- [Metadaten-Editor (XLSM) herunterladen](Metadaten-Editor.xlsm)
- Empfohlene App-Version: 
    - Desktop-Version von Excel aus den Office 365 (Business) / Microsoft 365 (Business) Plänen

Diese Excel-Datei kann für die strukturierte Erfassung und Aktualisierung von Metadaten für digitale Inhalte verwendet werden.
Die Datei nutzt Makros und externe Datenverbindungen zur Vereinfachung und Automatisierung, z.B. zur Aktualisierung der kontrollierten Vokabulare.

Überblick:
1. Tabellenblatt „Start“ zeigt eine Übersicht über die Bearbeitungsschritte.
2. Tabellenblatt "UrheberInnen" dient der Erfassung von IDs oder Namen/Bezeichnungen von UrheberInnen (Personen und Organisationen).
    * Mögliche ID-Typen:
        * [GND-ID](https://d-nb.info/gnd) → Spalte `GNDID`
        * [ROR-ID](https://ror.org) → Spalte `RORID`
        * [ORC-ID](https://orcid.org) → Spalte `ORCID`
        * [Wikidata-ID](https://wikidata.org) → Spalte `WIKIDATA`
        * Alternativ dazu: Name/Beschreibung in Spalte `COMMON_NAME`
3. Tabellenblatt "Anbieter" ermöglicht die Erfassung einiger grundlegender Informationen über den Anbieter.
4. Tabellenblatt „Stichwörter“ ermöglicht die Eingabe von Stichwörtern für eine strukturierte Auswahl von Inhalten.
5. Tabellenblatt „Metadaten“ ermöglicht die Erfassung von Metadaten zu Inhalten (z.B. Unterrichtsvideos, Bildungsangeboten).

