import argparse
from pathlib import Path


def overlay_pdfs(base_pdf: Path, overlay_pdf: Path, output_pdf: Path) -> None:
	from pypdf import PdfReader, PdfWriter

	base_reader = PdfReader(str(base_pdf))
	overlay_reader = PdfReader(str(overlay_pdf))
	writer = PdfWriter()

	if len(overlay_reader.pages) == 0:
		raise ValueError(f"Overlay PDF has no pages: {overlay_pdf}")

	# If the overlay has fewer pages, reuse its first page as frame for remaining pages.
	for i, base_page in enumerate(base_reader.pages):
		overlay_page = overlay_reader.pages[i] if i < len(overlay_reader.pages) else overlay_reader.pages[0]
		base_page.merge_page(overlay_page)
		writer.add_page(base_page)

	output_pdf.parent.mkdir(parents=True, exist_ok=True)
	with output_pdf.open("wb") as f:
		writer.write(f)


def main() -> None:
	parser = argparse.ArgumentParser(description="Overlay one PDF onto another.")
	parser.add_argument("base_pdf", type=Path, help="PDF to use as the base document")
	parser.add_argument("overlay_pdf", type=Path, help="PDF to place over the base document")
	parser.add_argument("output_pdf", type=Path, help="Path for the merged output PDF")
	args = parser.parse_args()

	overlay_pdfs(args.base_pdf, args.overlay_pdf, args.output_pdf)
	print(f"Created: {args.output_pdf}")


if __name__ == "__main__":
	main()
