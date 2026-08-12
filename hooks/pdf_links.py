"""Add a download button when a note has a same-named PDF beside it."""

from pathlib import Path
from urllib.parse import quote


def on_page_markdown(markdown, *, page, config, files):
    source = Path(page.file.abs_src_path)
    pdf = source.with_suffix(".pdf")
    if not pdf.is_file():
        return markdown

    pdf_url = quote(pdf.name)
    button = (
        f"\n\n[:material-file-pdf-box: 在线查看或下载配套 PDF]"
        f"(./{pdf_url}){{ .md-button .pdf-download }}\n"
    )

    lines = markdown.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("# "):
            lines.insert(index + 1, button)
            return "".join(lines)

    return button.lstrip() + "\n" + markdown
