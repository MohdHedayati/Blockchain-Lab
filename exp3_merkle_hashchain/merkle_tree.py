"""Experiment 3.1 - Merkle tree of 10 academic transactions."""
import hashlib, random

random.seed(42)
SUBJECTS = ["Maths", "Physics", "Algorithms", "Databases", "Networks"]
GRADES = ["AA", "AB", "BB", "BC", "CC"]


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def make_transactions(n=10):
    """Student 241080023 gets grades for 5 subjects per semester (10 txs = 2 semesters)."""
    txs = []
    for i in range(n):
        sem = i // 5 + 1
        subj = SUBJECTS[i % 5]
        txs.append(f"TX{i + 1}|student=241080023|sem={sem}|subject={subj}|grade={random.choice(GRADES)}")
    return txs


def build_merkle_tree(leaves):
    """Returns list of levels, level 0 = leaf hashes, last level = [root]."""
    level = [sha256(t) for t in leaves]
    levels = [level]
    while len(level) > 1:
        if len(level) % 2 == 1:           # odd count: duplicate last node
            level = level + [level[-1]]
        level = [sha256(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        levels.append(level)
    return levels


if __name__ == "__main__":
    txs = make_transactions(10)
    print("=== Transactions ===")
    for t in txs:
        print(t)
    levels = build_merkle_tree(txs)
    print("\n=== Merkle Tree ===")
    for i, lvl in enumerate(levels):
        name = "Leaf hashes" if i == 0 else ("ROOT" if len(lvl) == 1 else f"Level {i}")
        print(f"\n{name}:")
        for h in lvl:
            print("  ", h)
    print("\nMerkle Root (digital fingerprint of all 10 transactions):")
    print(levels[-1][0])

    # tamper demo
    txs[3] = txs[3].replace("grade=", "grade=X")
    print("\nAfter tampering with TX4, root =", build_merkle_tree(txs)[-1][0])
