"""
Part C – Question 5: Performance and Scalability
Implements optimization, parallel processing, and memory-efficient analysis tools.
"""

import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from fasta_handler import parse_fasta


def process_sequence(record):
    """Example heavy computation: GC content calculation."""
    seq = record.sequence
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    time.sleep(0.2)  # simulate heavy computation
    return record.header, round(gc, 3)


def analyze_fasta_parallel(fasta_file, workers=4):
    """Analyze sequences in parallel and show progress."""
    results = []
    records = list(parse_fasta(fasta_file))
    total = len(records)

    print(f"🚀 Analyzing {total} sequences using {workers} threads…")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_rec = {executor.submit(process_sequence, r): r for r in records}
        done = 0
        for future in as_completed(future_to_rec):
            header, gc = future.result()
            results.append((header, gc))
            done += 1
            print(f"Progress: {done}/{total} – {header} GC = {gc}")

    return results


def memory_efficient_reader(fasta_file):
    """Generator that reads FASTA sequences line by line to save RAM."""
    with open(fasta_file, "r") as file:
        header, seq = None, []
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    yield header, "".join(seq)
                header = line[1:]
                seq = []
            else:
                seq.append(line)
        if header:
            yield header, "".join(seq)


def performance_test(fasta_file):
    """Measure execution time and estimate memory usage."""
    start = time.time()
    results = analyze_fasta_parallel(fasta_file)
    end = time.time()

    print("\n⏱ Time taken: ", round(end - start, 3), "seconds")
    print("💾 Approx memory used (by file): ", os.path.getsize(fasta_file) / 1024, "KB")
    return results


if __name__ == "__main__":
    sample_file = "sample.fasta"
    print("⚙️ Running performance test on :", sample_file)
    performance_test(sample_file)
