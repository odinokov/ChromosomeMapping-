#!/usr/bin/env python3
"""
Chromosome ReMapping Script

This script remaps chromosome names in the BAM file header based on a provided mapping file.

Usage:
    1) Get mapping files (chromosome/contig name mappings between UCSC <-> Ensembl <-> Gencode for a variety of genomes):
       git clone https://github.com/dpryan79/ChromosomeMappings
    2) Remap chromosomes:
       samtools view -H "$in_bam" | python remap.py "$mapping_file" | samtools reheader - "$in_bam" > "$out_bam"

Where:
    "$mapping_file" is the path to a file containing the chromosome mappings.
"""

import sys
import re
import argparse
from typing import Dict


class ChromosomeRemapper:
    """
    A class to handle the remapping of chromosome names in BAM file headers based on a provided mapping file.
    """

    # Compile the regular expression pattern once for efficiency
    SN_TAG_PATTERN = re.compile(r'\bSN:(\S+)')

    def __init__(self, mapping_file: str):
        """
        Initialize the ChromosomeRemapper with a mapping file.

        Args:
            mapping_file (str): Path to the chromosome mapping file.
        """
        self.mapping_file = mapping_file
        self.mapping_dict = self.load_chromosome_mappings()

    def load_chromosome_mappings(self) -> Dict[str, str]:
        """
        Load chromosome mappings from a file into a dictionary.
        Retain the original chromosome name if the mapping value is absent.

        Returns:
            Dict[str, str]: A dictionary with original chromosome names as keys and remapped names as values.
        """
        mapping = {}
        try:
            with open(self.mapping_file, "r") as file:
                for line_number, line in enumerate(file, start=1):
                    parts = line.strip().split("\t")
                    if not parts or len(parts[0].strip()) == 0:
                        # Skip empty or invalid lines
                        continue
                    original = parts[0]
                    remapped = parts[1] if len(parts) > 1 and parts[1].strip() else original
                    mapping[original] = remapped
        except FileNotFoundError:
            print(f"Error: File '{self.mapping_file}' not found.", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"Error reading file '{self.mapping_file}': {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error while loading mappings: {e}", file=sys.stderr)
            sys.exit(1)
        return mapping

    def replace_sn(self, match: re.Match) -> str:
        """
        Replacement function for SN tag using regex substitution.

        Args:
            match (re.Match): The regex match object.

        Returns:
            str: The replaced SN tag with remapped chromosome name.
        """
        original_chrom = match.group(1)
        remapped_chrom = self.mapping_dict.get(original_chrom, original_chrom)
        return f"SN:{remapped_chrom}"

    def remap_chromosome_in_line(self, line: str) -> str:
        """
        Remap chromosome name in the given line using the provided mapping dictionary.

        Args:
            line (str): A single line from the BAM header.

        Returns:
            str: The line with the chromosome name remapped if applicable.
        """
        if line.startswith("@SQ"):
            # Substitute only the SN tag using the replace_sn callback
            remapped_line = self.SN_TAG_PATTERN.sub(self.replace_sn, line)
            return remapped_line
        return line

    def process_genomic_data(self):
        """
        Process each line of the input BAM header and remap chromosome names.
        """
        for line_number, header_line in enumerate(sys.stdin, start=1):
            header_line = header_line.rstrip('\n')
            remapped_line = self.remap_chromosome_in_line(header_line)
            print(remapped_line)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Remap chromosome names in BAM file headers based on a provided mapping file.\n\n"
            "Usage:\n"
            "  samtools view -H <input.bam> | python remap.py <mapping_file> | samtools reheader - <input.bam> > <output.bam>"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "mapping_file",
        help="Path to the chromosome mapping file."
    )
    return parser.parse_args()


def main():
    """
    Main function to execute the chromosome remapping process.
    """
    args = parse_arguments()
    remapper = ChromosomeRemapper(args.mapping_file)
    remapper.process_genomic_data()


if __name__ == "__main__":
    main()
