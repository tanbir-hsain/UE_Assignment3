"""
Part B – Question 3: Multiple Sequence Problems
Implements basic sequence alignment, common subsequence detection,
consensus sequence generation, and evolutionary distance calculation.
"""

from itertools import combinations


def pairwise_alignment(seq1, seq2, match=1, mismatch=-1, gap=-2):
    """Simple Needleman-Wunsch pairwise alignment (global)."""
    n, m = len(seq1), len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i * gap
    for j in range(m + 1):
        dp[0][j] = j * gap

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = dp[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            delete = dp[i - 1][j] + gap
            insert = dp[i][j - 1] + gap
            dp[i][j] = max(match_score, delete, insert)

    return dp[n][m]


def longest_common_subsequence(seq1, seq2):
    """Find the longest common subsequence (LCS) of two sequences."""
    n, m = len(seq1), len(seq2)
    dp = [[""] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + seq1[i - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], key=len)

    return dp[-1][-1]


def consensus_sequence(sequences):
    """Generate a consensus sequence from multiple aligned sequences."""
    if not sequences:
        return ""
    length = len(sequences[0])
    consensus = ""

    for i in range(length):
        column = [seq[i] for seq in sequences if i < len(seq)]
        base = max(set(column), key=column.count)
        consensus += base

    return consensus


def evolutionary_distance(seq1, seq2):
    """Calculate a simple evolutionary distance (proportion of mismatches)."""
    length = min(len(seq1), len(seq2))
    mismatches = sum(1 for a, b in zip(seq1, seq2) if a != b)
    return mismatches / length


if __name__ == "__main__":
    sequences = ["ATGCTAGC", "ATGCGAGC", "ATGCTTGC"]

    print("🔬 Pairwise Alignment Score:")
    print(pairwise_alignment(sequences[0], sequences[1]))

    print("\n🧩 Longest Common Subsequence:")
    print(longest_common_subsequence(sequences[0], sequences[2]))

    print("\n🧬 Consensus Sequence:")
    print(consensus_sequence(sequences))

    print("\n🌳 Evolutionary Distance:")
    print(evolutionary_distance(sequences[0], sequences[1]))

