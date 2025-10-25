"""
Part B – Question 4: Advanced Pattern Analysis
Implements pattern matching, repeats, palindromes, assembly simulation,
and simple phylogenetic similarity analysis.
"""

from itertools import combinations


def find_repeats(sequence, length=4):
    """Find repeated substrings of a given length."""
    repeats = {}
    for i in range(len(sequence) - length + 1):
        sub = sequence[i:i + length]
        repeats[sub] = repeats.get(sub, 0) + 1
    return {k: v for k, v in repeats.items() if v > 1}


def find_palindromes(sequence, min_len=4):
    """Find palindromic regions (reads same forward/backward)."""
    pals = []
    for i in range(len(sequence)):
        for j in range(i + min_len, len(sequence) + 1):
            sub = sequence[i:j]
            if sub == sub[::-1]:
                pals.append(sub)
    return pals


def assemble_fragments(fragments):
    """Simulate simple sequence assembly by overlapping fragments."""
    assembled = fragments[0]
    for frag in fragments[1:]:
        overlap_found = False
        for i in range(len(frag)):
            if assembled.endswith(frag[:i]):
                assembled += frag[i:]
                overlap_found = True
                break
        if not overlap_found:
            assembled += frag
    return assembled


def phylogenetic_similarity(sequences):
    """Generate a simple similarity matrix for given sequences."""
    def similarity(a, b):
        length = min(len(a), len(b))
        return sum(x == y for x, y in zip(a, b)) / length

    matrix = {}
    for (name1, seq1), (name2, seq2) in combinations(sequences.items(), 2):
        score = similarity(seq1, seq2)
        matrix[(name1, name2)] = round(score, 3)
    return matrix


if __name__ == "__main__":
    seq = "ATGCATGCATTTATGCATGCAT"
    print("🧩 Repeats (length=4):")
    print(find_repeats(seq))

    print("\n🔁 Palindromic Sequences:")
    print(find_palindromes("ATGCGAATTCGCAT"))

    print("\n🧬 Assembled Sequence:")
    fragments = ["ATGCG", "GCGTA", "GTATT"]
    print(assemble_fragments(fragments))

    print("\n🌳 Phylogenetic Similarity Matrix:")
    seqs = {
        "Seq1": "ATGCTAGC",
        "Seq2": "ATGCGAGC",
        "Seq3": "TTGCTAGT"
    }
    print(phylogenetic_similarity(seqs))
