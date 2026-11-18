"""Experiment 5 - Proof of Work consensus: mine a block per record until
SHA256(block header) has `difficulty` leading zeros. Blocks are chained by previous hash."""
import hashlib, json, time

DIFFICULTY = 5          # number of leading hex zeros required
RECORDS = [
    "Veermata Jijabai Technological Institute",
    "Computer Engineering and Information Technology",
    "Blockchain Technology",
    "241080023",
]


class Block:
    def __init__(self, index, data, prev_hash):
        self.index, self.data, self.prev_hash = index, data, prev_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        header = json.dumps([self.index, self.timestamp, self.data, self.prev_hash, self.nonce])
        return hashlib.sha256(header.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        start = time.time()
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()
        return time.time() - start


class Blockchain:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        genesis = Block(0, "Genesis Block", "0" * 64)
        genesis.mine(difficulty)
        self.chain = [genesis]

    def add_block(self, data):
        b = Block(len(self.chain), data, self.chain[-1].hash)
        secs = b.mine(self.difficulty)
        self.chain.append(b)
        return b, secs

    def is_valid(self):
        for i, b in enumerate(self.chain):
            if b.hash != b.compute_hash() or not b.hash.startswith("0" * self.difficulty):
                return False
            if i and b.prev_hash != self.chain[i - 1].hash:
                return False
        return True


if __name__ == "__main__":
    print(f"Proof of Work - difficulty = {DIFFICULTY} leading zeros (target: {'0' * DIFFICULTY}...)\n")
    bc = Blockchain(DIFFICULTY)
    g = bc.chain[0]
    print(f"Block 0 (genesis) nonce={g.nonce}\n  hash: {g.hash}\n")
    for i, rec in enumerate(RECORDS, 1):
        b, secs = bc.add_block(f"Record{i} - {rec}")
        print(f"Block {b.index}  data: {b.data}")
        print(f"  prev : {b.prev_hash}")
        print(f"  nonce: {b.nonce}   mined in {secs:.2f}s")
        print(f"  hash : {b.hash}\n")
    print("Blockchain valid?", bc.is_valid())
    bc.chain[2].data = "Record2 - TAMPERED"
    print("After tampering with Block 2 data, valid?", bc.is_valid())
