"""
Genomic Data Integration
Part A – Question 2
Handles genomic sequence storage, validation, and retrieval using SQLite.
"""

import sqlite3
import re
from fasta_handler import parse_fasta


class GenomicDatabase:
    """A simple database for storing and retrieving genomic sequences."""

    def __init__(self, db_name="genomic_data.db"):
        """Initialize and connect to the database."""
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Create a table for sequences if not already present."""
        query = """
        CREATE TABLE IF NOT EXISTS sequences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            header TEXT UNIQUE,
            sequence TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def validate_sequence(self, sequence):
        """Check if a DNA sequence only contains valid bases."""
        return bool(re.fullmatch(r"[ATGC]+", sequence.upper()))

    def insert_sequence(self, header, sequence):
        """Insert a validated sequence into the database."""
        if not self.validate_sequence(sequence):
            print(f"❌ Invalid sequence for {header}: contains non-ATGC characters.")
            return False
        try:
            query = "INSERT INTO sequences (header, sequence) VALUES (?, ?)"
            self.conn.execute(query, (header, sequence))
            self.conn.commit()
            print(f"✅ Inserted: {header}")
            return True
        except sqlite3.IntegrityError:
            print(f"⚠️ Sequence with header '{header}' already exists.")
            return False

    def search_sequence(self, keyword):
        """Search for sequences whose header contains the given keyword."""
        query = "SELECT header, sequence FROM sequences WHERE header LIKE ?"
        cursor = self.conn.execute(query, (f"%{keyword}%",))
        results = cursor.fetchall()
        return results

    def display_all(self):
        """Display all sequences in the database."""
        cursor = self.conn.execute("SELECT header, sequence FROM sequences")
        return cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()


if __name__ == "__main__":
    # Example usage
    db = GenomicDatabase()

    print("\n📂 Loading sequences from FASTA file...")
    fasta_file = "sample.fasta"  # File created from your previous code

    for record in parse_fasta(fasta_file):
        db.insert_sequence(record.header, record.sequence)

    print("\n🔍 Searching for 'seq1':")
    results = db.search_sequence("seq1")
    for header, seq in results:
        print(f"Found: {header} -> {seq}")

    print("\n📜 All sequences in database:")
    for header, seq in db.display_all():
        print(f"{header}: {seq}")

    db.close()

