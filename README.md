# Chromosome Mapping Script

## Overview
Remaps chromosome names in genomic data using a provided mapping file.

## Prerequisites
- Python 3.x
- Samtools
- Chromosome mapping files `git clone https://github.com/dpryan79/ChromosomeMappings`
- Genomic data in BAM format

## Usage
```
samtools view -H "$in_bam" | python remap.py "$mapping_file" | samtools reheader - "$in_bam"
```
Where:
- `$in_bam`: Input BAM file
- `$mapping_file`: Chromosome mapping file
- `$out_bam`: Output BAM file
