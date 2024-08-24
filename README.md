# Quick PDF Converter and Merger

A simple script I wrote to quickly convert various document formats to PDF and merge PDFs. It's not fancy, but it gets the job done when I need it every couple of months.

## What it does

- Converts .doc, .docx, .ppt, and .pptx files to PDF
- Merges multiple PDFs into one
- Works from the command line

## Requirements

- Python 3.7+
- LibreOffice (for converting docs)
- PyPDF2 and Click (Python libraries)

## Quick Start

1. Clone or download this repo
2. Install the required Python libraries:
   ```
   pip install PyPDF2 click
   ```
3. Make sure LibreOffice is installed on your system

## How to Use

### Basic Usage

Convert files:
```
python converter.py convert /path/to/docs /path/for/output
```

Merge PDFs:
```
python converter.py merge /path/to/pdfs output.pdf
```

### With Just (if you have it installed)

Convert:
```
just convert
```

Merge:
```
just merge output.pdf
```

Convert and merge:
```
just convert-and-merge final.pdf
```

## Notes

- This is a personal script, so it might need tweaking for your setup
- It's not extensively tested or error-proofed
- Feel free to modify it to suit your needs

## Troubleshooting

If something doesn't work:
1. Check if LibreOffice is installed and accessible from command line
2. Make sure you have the right Python libraries installed
3. Double-check your file paths

That's pretty much it. Hope it's useful!
