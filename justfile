# Default source and output directories
default_source_dir := "."
default_output_dir := ".converted"

# Convert files to PDF
convert source_dir=default_source_dir output_dir=default_output_dir:
    uv run ./converter.py convert {{source_dir}} {{output_dir}}

# Merge PDF files
merge output_file output_dir=default_output_dir:
    uv run ./converter.py merge {{output_dir}} {{output_file}}

# Convert and then merge
convert-and-merge output_file source_dir=default_source_dir output_dir=default_output_dir: (convert source_dir output_dir)
    @just merge {{output_file}} {{output_dir}}

# Default rule to show available commands
default:
    @echo "Available commands:"
    @just --list
