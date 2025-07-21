Language: [Deutsch](README.md), [Englisch](README_EN.md)

# Providing metadata
Any databases / data sources can be used to provide metadata.
A supported export format is RSS/XML feeds in accordance with the [specifications](../README.md).

## Excel Editor
The metadata editor template for Microsoft Office can be used to record metadata.

- [Download the Metadata Editor (XLSM)](Metadata-Editor.xlsm)
- Recommended app version: 
    - Desktop version of Excel from the Office 365 (Business) / Microsoft 365 (Business) plans

This Excel file can be used for the structured recording and updating of metadata for digital content.
The file uses macros and external data connections for simplification and automation, e.g. to update the controlled vocabularies.

Overview:
1. Worksheet “Start” shows an overview of the editing steps.
2. Worksheet "Creators" (UrheberInnen) is used to record IDs or names/designations of creators (persons and organizations).
    * Possible ID types:
        * [GND-ID](https://d-nb.info/gnd) → column `GNDID`
        * [ROR-ID](https://ror.org) → column `RORID`
        * [ORC-ID](https://orcid.org) → Column `ORCID`
        * [Wikidata-ID](https://wikidata.org) → Column `WIKIDATA`
        * Alternatively: Name/description in column `COMMON_NAME`
3. Worksheet “Provider” (Anbieter) records some basic information about the provider.
4. Worksheet “Keywords” (Stichwörter) enables the entry of keywords for a structured selection of content.
5. Worksheet “Metadata” (Metadaten) enables the recording of metadata for content.

The metadata can be exported as XML in accordance with the specifications.
This XML file can then be provided as a URL for the meta video portal.