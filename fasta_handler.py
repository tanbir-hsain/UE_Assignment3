"""
Part A – FASTA File Processing and Genomic Data Integration
------------------------------------------------------------
This module handles:
- FASTA file parsing
- Sequence storage and retrieval
- Searching within sequences
- Writing new FASTA files

Author: [Your Name]
Assignment: Genomic Databases and Advanced Applications (CCA5)
"""

import os

class SequenceRecord:
    """A class to represent a single FASTA record."""
    def __init__(self, header, sequence):
        self.header = header.strip()
        self.sequence = sequence.replace("\n", "").strip()

    def __repr__(self):
        return f"SequenceRecord(header={self.header}, length={len(self.sequence)})"


def parse_fasta(file_path):
    """
    Parse a FASTA file and yield SequenceRecord objects.

    Args:
        file_path (str): Path to the FASTA file.

    Yields:
        SequenceRecord: Object containing header and sequence.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    header = None
    seq_lines = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    yield SequenceRecord(header, "".join(seq_lines))
                header = line[1:]  # remove '>'
                seq_lines = []
            else:
                seq_lines.append(line)
        if header:
            yield SequenceRecord(header, "".join(seq_lines))


def write_fasta(records, output_path):
    """
    Write a list of SequenceRecord objects into a FASTA file.

    Args:
        records (list): List of SequenceRecord objects.
        output_path (str): File path to save the FASTA file.
    """
    with open(output_path, "w") as file:
        for record in records:
            file.write(f">{record.header}\n")
            # Break long lines for readability
            for i in range(0, len(record.sequence), 60):
                file.write(record.sequence[i:i+60] + "\n")


def search_sequence(fasta_file, keyword):
    """
    Search for sequences in a FASTA file that contain a specific keyword.

    Args:
        fasta_file (str): Path to the FASTA file.
        keyword (str): The text to search for in sequence headers or sequences.

    Returns:
        list: Matching SequenceRecord objects.
    """
    matches = []
    with open(fasta_file, "r") as file:
        header = None
        seq = []
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if header and keyword.lower() in "".join(seq).lower():
                    matches.append(SequenceRecord(header, "".join(seq)))
                header = line[1:]
                seq = []
            else:
                seq.append(line)
        if header and keyword.lower() in "".join(seq).lower():
            matches.append(SequenceRecord(header, "".join(seq)))
    return matches


def validate_fasta(file_path):
    """
    Check if a file is a valid FASTA format.

    Args:
        file_path (str): Path to file.

    Returns:
        bool: True if valid FASTA, False otherwise.
    """
    try:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            return first_line.startswith(">")
    except Exception:
        return False
