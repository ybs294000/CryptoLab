from __future__ import annotations

import os
import sys
import time
import unittest
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.generate_sample_files import ensure_sample_files


REPORT_PATH = REPO_ROOT / "tests" / "TEST_REPORT.md"


@dataclass
class TestRecord:
    name: str
    status: str
    detail: str = ""


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.records: list[TestRecord] = []

    def addSuccess(self, test) -> None:
        super().addSuccess(test)
        self.records.append(TestRecord(test.id(), "PASS"))

    def addFailure(self, test, err) -> None:
        super().addFailure(test, err)
        self.records.append(TestRecord(test.id(), "FAIL", self._exc_info_to_string(err, test)))

    def addError(self, test, err) -> None:
        super().addError(test, err)
        self.records.append(TestRecord(test.id(), "ERROR", self._exc_info_to_string(err, test)))

    def addSkip(self, test, reason) -> None:
        super().addSkip(test, reason)
        self.records.append(TestRecord(test.id(), "SKIP", reason))


def write_report(result: RecordingResult, duration_s: float) -> None:
    ensure_sample_files()
    lines = [
        "# CryptoLab Test Report",
        "",
        f"- Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Python: {sys.version.split()[0]}",
        f"- Duration: {duration_s:.2f}s",
        f"- Total tests: {result.testsRun}",
        f"- Passed: {sum(1 for r in result.records if r.status == 'PASS')}",
        f"- Failed: {len(result.failures)}",
        f"- Errors: {len(result.errors)}",
        f"- Skipped: {len(result.skipped)}",
        "",
        "## Results",
        "",
        "| Test | Status | Notes |",
        "|---|---|---|",
    ]

    for record in sorted(result.records, key=lambda r: r.name):
        note = record.detail.splitlines()[0] if record.detail else ""
        note = note.replace("|", "\\|")
        lines.append(f"| `{record.name}` | {record.status} | {note} |")

    if result.failures or result.errors:
        lines.extend(["", "## Failure Details", ""])
        for record in result.records:
            if record.status not in {"FAIL", "ERROR"}:
                continue
            lines.append(f"### `{record.name}`")
            lines.append("")
            lines.append("```text")
            lines.append(record.detail.rstrip())
            lines.append("```")
            lines.append("")

    REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    os.chdir(REPO_ROOT)
    ensure_sample_files()
    loader = unittest.defaultTestLoader
    suite = loader.discover("tests", pattern="test_*.py")

    start = time.perf_counter()
    runner = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult)
    result: RecordingResult = runner.run(suite)
    duration_s = time.perf_counter() - start
    write_report(result, duration_s)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
