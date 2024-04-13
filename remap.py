##!/usr/bin/env python3
"""
Chromosome ReMapping Script

This script remaps chromosome names in the BAM file header based on a provided mapping file.

Usage:
    1) get mapping files: git clone https://github.com/dpryan79/ChromosomeMappings
    2) remap chromosomes: samtools view -H "$in_bam" | python remap.py "$mapping_file" | samtools reheader - "$in_bam" > "$out_bam"
    
Where:
    "$mapping_file" is the path to a file containing the chromosome mappings.
"""

import sys
import os
from typing import Dict

def load_chromosome_mappings(file_path: str) -> Dict[str, str]:
    """
    Load chromosome mappings from a file into a dictionary.
    Retain the mapping key as a value if the mapping value is absent.
    """
    mapping = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                original, *mapped = line.strip().split('\t')
                mapping[original] = mapped[0] if mapped else original
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    return mapping

def remap_chromosome_in_line(line: str, mapping_dict: Dict[str, str]) -> str:
    """
    Remap chromosome name in the given line using the provided mapping dictionary.
    """
    if line.startswith('@SQ'):
        for original, remapped in mapping_dict.items():
            if f'\tSN:{original}\t' in line:
                return line.replace(f'\tSN:{original}\t', f'\tSN:{remapped}\t')
    return line

def process_genomic_data(mapping_file: str):
    """
    Process each line of the input file and remap chromosome names.
    """
    chromosome_mapping = load_chromosome_mappings(mapping_file)
    for header_line in sys.stdin:
        print(remap_chromosome_in_line(header_line.strip(), chromosome_mapping))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        script_name = os.path.basename(__file__)
        print("Incorrect usage.", file=sys.stderr)
        sys.exit(1)

    chromosome_mapping_file = sys.argv[1]
    process_genomic_data(chromosome_mapping_file)
