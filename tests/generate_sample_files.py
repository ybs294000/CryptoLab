"""
Generate stable sample files used by the CryptoLab test suite.
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
ASSETS_DIR = REPO_ROOT / "assets"


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def create_minimal_pdf(path: Path) -> None:
    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 144]/Contents 4 0 R/Resources<<>> >>endobj\n"
        b"4 0 obj<</Length 44>>stream\n"
        b"BT /F1 18 Tf 36 96 Td (CryptoLab test PDF) Tj ET\n"
        b"endstream endobj\n"
        b"xref\n0 5\n0000000000 65535 f \n"
        b"0000000010 00000 n \n0000000053 00000 n \n0000000109 00000 n \n0000000208 00000 n \n"
        b"trailer<</Size 5/Root 1 0 R>>\nstartxref\n302\n%%EOF\n"
    )
    _write_bytes(path, pdf_bytes)


def create_minimal_xlsx(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>""",
        )
        zf.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>""",
        )
        zf.writestr(
            "docProps/core.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>CryptoLab Test Workbook</dc:title>
</cp:coreProperties>""",
        )
        zf.writestr(
            "docProps/app.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>CryptoLab Tests</Application>
</Properties>""",
        )
        zf.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>""",
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>""",
        )
        zf.writestr(
            "xl/worksheets/sheet1.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>CryptoLab</t></is></c>
      <c r="B1" t="inlineStr"><is><t>Test</t></is></c>
    </row>
  </sheetData>
</worksheet>""",
        )


def ensure_sample_files() -> dict[str, Path]:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

    logo_src = ASSETS_DIR / "logo1.png"
    logo_dst = FIXTURES_DIR / "sample_logo.png"
    if logo_src.exists():
        shutil.copyfile(logo_src, logo_dst)

    text_path = FIXTURES_DIR / "sample_text.txt"
    _write_text(
        text_path,
        "CryptoLab sample text file.\nAES and ChaCha20 protect bytes, not just words.\n",
    )

    pdf_path = FIXTURES_DIR / "sample_document.pdf"
    create_minimal_pdf(pdf_path)

    xlsx_path = FIXTURES_DIR / "sample_sheet.xlsx"
    create_minimal_xlsx(xlsx_path)

    bin_path = FIXTURES_DIR / "sample_payload.bin"
    _write_bytes(bin_path, bytes(range(256)))

    return {
        "logo": logo_dst,
        "text": text_path,
        "pdf": pdf_path,
        "xlsx": xlsx_path,
        "bin": bin_path,
    }


if __name__ == "__main__":
    created = ensure_sample_files()
    for name, path in created.items():
        print(f"{name}: {path}")
