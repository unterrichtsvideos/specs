# XML-Validator-Tool
Ein CLI-Tool zur Validierung von XML-Dateien gegen ein XSD-Schema mit [xmlschema](https://pypi.org/project/xmlschema/).
Geeignet für: CI-Pipelines, Pre-Commit-Hooks und lokale Workflows,

## Anforderungen

- [Download](https://github.com/unterrichtsvideos/specs/tree/main/scripts)

Das Tool erfordert **Python 3.10+** und `xmlschema`:

```sh
pip install -r requirements.txt
```

## Verwendungsbeispiel
Um XML-Feeds in ./feeds mit dem neuesten XML-Schema von unterrichtsvideos.net zu validieren:

```sh
python scripts/validate.py --schema https://w3id.org/unterrichtsvideos.net/specs/latest/schema/mvp.xsd
```

Beispiel-XML-Feeds
```sh
python scripts/validate.py --glob ../version/draft/examples/**/*.xml --schema https://w3id.org/unterrichtsvideos.net/specs/latest/schema/mvp.xsd
```

### CLI-Parameter

| Option            | Beschreibung                                                           |
| ----------------- | --------------------------------------------------------------------- |
| `--schema PATH`   | Pfad oder HTTP(S)-URL zum XSD-Schema (Standard: `mvp.xsd`).         |
| `--glob PATTERN`  | Glob-Muster zur Auswahl von XML-Dateien (Standard: `feeds/**/*.xml`).  |
| `-q`, `--quiet`   | Nur Fehler und Zusammenfassung anzeigen.                              |
| `-v`, `--verbose` | Detaillierte Debugging-Informationen anzeigen.                       |

## Exit-Codes

| Code | Bedeutung                                                                                        |
| ---- | ---------------------------------------------------------------------------------------------- |
| `0`  | Alle XML-Dateien erfolgreich validiert                                                           |
| `1`  | Ein oder mehrere Fehler aufgetreten (fehlendes Schema, Validierungsfehler, keine passenden XML-Dateien usw.) |
