#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any, Dict, List, Iterable, Optional, Union
from urllib.parse import urlparse
from functools import lru_cache
import importlib


LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Dependency provider
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_xmlschema_module():
    """Load xmlschema dependency"""
    try:
        return importlib.import_module("xmlschema")
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: xmlschema. Install with 'pip install xmlschema'."
        ) from exc


# ---------------------------------------------------------------------------
# Schema Loading
# ---------------------------------------------------------------------------

class SchemaLoader:
    """Resolve and load XML Schema definitions."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def resolve_location(self, schema: str) -> Union[Path, str]:
        """Return absolute path or URL for the schema."""
        parsed = urlparse(schema)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return schema

        schema_path = Path(schema)
        if not schema_path.is_absolute():
            schema_path = (self.repo_root / schema_path).resolve()
        return schema_path

    def load(self, ref: Union[Path, str]) -> Any:
        """Load and return an xmlschema.XMLSchema instance."""
        module = load_xmlschema_module()
        xmlschema_exception = getattr(module, "XMLSchemaException", Exception)

        if isinstance(ref, Path) and not ref.is_file():
            raise FileNotFoundError(f"Schema not found: {ref}")

        try:
            return module.XMLSchema(ref)
        except (OSError, xmlschema_exception) as exc:
            raise RuntimeError(f"Failed to load schema from '{ref}'") from exc


# ---------------------------------------------------------------------------
# Error Formatter
# ---------------------------------------------------------------------------

class ValidationErrorFormatter:
    """Formats xmlschema validation errors for output/logging."""

    @staticmethod
    def format_error(err: Any) -> str:
        parts: List[str] = []

        pos = getattr(err, "position", None)
        if pos:
            try:
                line, col = pos
                parts.append(f"line {line}, column {col}")
            except Exception:
                parts.append(f"position {pos!r}")

        path = getattr(err, "path", None) or "/"
        parts.append(f"path {path}")

        reason = getattr(err, "reason", None) or getattr(err, "message", str(err))
        parts.append(str(reason))

        return " | ".join(parts)


# ---------------------------------------------------------------------------
# XML File Collection
# ---------------------------------------------------------------------------

class XMLFileCollector:
    """Collects XML files from the project tree."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def collect(self, pattern: str) -> List[Path]:
        files = sorted(p for p in self.repo_root.glob(pattern) if p.is_file())
        LOGGER.debug("Glob '%s' matched %d file(s).", pattern, len(files))
        return files


# ---------------------------------------------------------------------------
# Validator Engine
# ---------------------------------------------------------------------------

class XMLValidator:
    """
    Validates XML files against a provided xmlschema.XMLSchema instance.
    """

    def __init__(
        self,
        schema: Any,
        formatter: Optional[ValidationErrorFormatter] = None
    ):
        self.schema = schema
        self.formatter = formatter or ValidationErrorFormatter()

    def validate(self, xml_files: Iterable[Path], repo_root: Path) -> Dict[Path, List[str]]:
        """
        Validate each XML file
        """
        failures: Dict[Path, List[str]] = {}

        for xml_path in xml_files:
            rel = xml_path.relative_to(repo_root)
            LOGGER.debug("Validating '%s'...", rel)

            raw_errors = list(self.schema.iter_errors(xml_path))
            if raw_errors:
                failures[rel] = [self.formatter.format_error(e) for e in raw_errors]

        return failures


# ---------------------------------------------------------------------------
# CLI Runner
# ---------------------------------------------------------------------------

class XMLValidatorCLI:
    """
    Orchestrates CLI parsing, logging configuration, schema loading,
    file collection, validation, and output.
    """

    def __init__(self):
        self.repo_root = Path(__file__).resolve().parent

    # ---- CLI Parsing -----------------------------------------------------

    @staticmethod
    def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Validate XML files against an XSD schema."
        )
        parser.add_argument(
            "--schema",
            default="mvp.xsd",
            help="Path or URL to XSD (default: %(default)s, relative to repo root).",
        )
        parser.add_argument(
            "--glob",
            default="feeds/**/*.xml",
            help="Glob pattern for XML files (relative to repo root).",
        )
        parser.add_argument(
            "-q", "--quiet",
            action="store_true",
            help="Only show warnings/errors."
        )
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Show debug output."
        )
        return parser.parse_args(argv)

    # ---- Logging ---------------------------------------------------------

    @staticmethod
    def configure_logging(quiet: bool, verbose: bool) -> None:
        if quiet:
            level = logging.WARNING
        elif verbose:
            level = logging.DEBUG
        else:
            level = logging.INFO

        logging.basicConfig(level=level, format="%(message)s")

    # ---- Run -------------------------------------------------------------

    def run(self, argv: Optional[List[str]] = None) -> int:
        args = self.parse_args(argv)
        self.configure_logging(args.quiet, args.verbose)

        # Prepare schema
        loader = SchemaLoader(self.repo_root)
        schema_ref = loader.resolve_location(args.schema)

        LOGGER.debug("Repo root: %s", self.repo_root)
        LOGGER.debug("Schema resolved to: %s", schema_ref)

        try:
            schema = loader.load(schema_ref)
        except (FileNotFoundError, RuntimeError) as exc:
            LOGGER.error(str(exc))
            return 1

        # Collect files
        collector = XMLFileCollector(self.repo_root)
        xml_files = collector.collect(args.glob)

        if not xml_files:
            LOGGER.error(
                "No XML files matched pattern '%s' at root %s.",
                args.glob, self.repo_root,
            )
            return 1

        # Validate
        validator = XMLValidator(schema)
        failures = validator.validate(xml_files, self.repo_root)

        # Report
        total = len(xml_files)
        failed = len(failures)

        for rel, errors in failures.items():
            LOGGER.error("[FAIL] %s", rel)
            for idx, err in enumerate(errors, 1):
                LOGGER.error("    %d. %s", idx, err)

        for xml_path in xml_files:
            rel = xml_path.relative_to(self.repo_root)
            if rel not in failures:
                LOGGER.info("[ OK ] %s", rel)

        if failed:
            LOGGER.error("%d/%d XML file(s) failed validation.", failed, total)
            return 1

        LOGGER.info("Validated %d XML file(s) successfully.", total)
        return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    cli = XMLValidatorCLI()
    return cli.run(argv)


if __name__ == "__main__":
    import sys
    sys.exit(main())
