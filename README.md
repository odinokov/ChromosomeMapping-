# Chromosome ReMapping Script

## Overview
This script enables the remapping of chromosome and contig names within the headers of BAM files.

## Prerequisites
To use this script, ensure you have the following:
- Python 3.x
- Samtools
- Chromosome mapping files, available via `git clone https://github.com/dpryan79/ChromosomeMappings`

## Usage
To remap chromosome names in your BAM file headers, use the following command:
```
samtools view -H "$in_bam" | python remap.py "$mapping_file" | samtools reheader - "$in_bam"
```
Where:
- `$in_bam`: is the path to your input BAM file.
- `$mapping_file`: refers to the chromosome mapping file you've obtained.
- `$out_bam`: is the path for the output BAM file with updated headers.
