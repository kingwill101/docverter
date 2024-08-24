#!/bin/env python

import os
import subprocess
import PyPDF2
import click
import shutil

class Converter(object):
    def __init__(self, source, dest):
        self.source = source
        self.destination = dest

    def convert(self):
        pass

class SOffice(Converter):
    def convert(self):
        destination_dir = os.path.dirname(self.destination)
        base_name = os.path.basename(self.source)
        name, _ = os.path.splitext(base_name)
        command = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", destination_dir, self.source]
        try:
            subprocess.run(command, check=True)

            # Look for the converted file
            for file in os.listdir(destination_dir):
                if file.startswith(name) and file.endswith('.pdf'):
                    original_output = os.path.join(destination_dir, file)
                    break
            else:
                raise FileNotFoundError(f"Converted file not found for {self.source}")

            # Rename the file to match the desired destination filename
            if original_output != self.destination:
                os.rename(original_output, self.destination)

            print(f"Converted {self.source} to {self.destination}")

        except subprocess.CalledProcessError as e:
            print(f"Error converting {self.source}: {e}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
class UnoConv(Converter):
    def convert(self):
        command = ["unoconv", "-o", self.source, self.destination]
        try:
            subprocess.run(command, check=True)
            print(f"Converted {self.source} to {self.destination}")

        except subprocess.CalledProcessError as e:
            print(f"Error converting {self.source}: {e}")

def convert_to_pdf(directory):
    pdf_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename.endswith((".docx", ".doc", ".ppt", ".pptx")):
                output_file = os.path.splitext(file_path)[0] + ".pdf"
                converter  = SOffice(file_path, output_file)
                converter.convert()
            elif filename.endswith(".pdf"):
                pdf_files.append(file_path)

    return pdf_files

def move_files(files, destination):
    for file in files:
        base_name = os.path.basename(file)
        final_destination = os.path.join(destination, base_name)

        if os.path.exists(final_destination):
            # Rename the file if it already exists
            name, ext = os.path.splitext(base_name)
            counter = 1
            new_name = f"{name}_{counter}{ext}"
            final_destination = os.path.join(destination, new_name)
            while os.path.exists(final_destination):
                counter += 1
                new_name = f"{name}_{counter}{ext}"
                final_destination = os.path.join(destination, new_name)

        try:
            print(f"moving {file} to {final_destination}")
            shutil.move(file, final_destination)
        except Exception as e:
            print(f"Error moving file {file} to {final_destination}: {e}")



def merge_pdfs(pdf_list, output_path):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        try:
            merger.append(pdf)
        except Exception as e:
            print(f"Error merging {pdf}: {e}")

    with open(output_path, 'wb') as output_file:
        merger.write(output_file)
    merger.close()
    print(f"Merged PDFs into {output_path}")

@click.group()
def cli():
    pass

@click.command()
@click.argument('directory', type=click.Path(exists=True))
@click.argument('destination', required=False)
def convert(directory, destination):
    """Converts files in the DIRECTORY to PDF. Optionally moves them to DESTINATION."""
    pdf_files = convert_to_pdf(directory)
    click.echo(f"Converted files in {directory}")

    if destination:
        if not os.path.exists(destination):
            os.makedirs(destination)
        move_files(pdf_files, destination)
        click.echo(f"Moved converted files to {destination}")

@click.command()
@click.argument('directory', type=click.Path(exists=True))
@click.argument('output_path')
def merge(directory, output_path):
    """Merges all PDF files in the DIRECTORY and saves to OUTPUT_PATH."""
    pdf_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pdf')]
    merge_pdfs(pdf_files, output_path)
    click.echo(f"Merged PDFs into {output_path}")

cli.add_command(convert)
cli.add_command(merge)

if __name__ == '__main__':
    cli()
