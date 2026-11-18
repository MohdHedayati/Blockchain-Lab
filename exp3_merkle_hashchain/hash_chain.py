"""Experiment 3.2 - Hash chain of grade-card PDFs.
chain_i = SHA256(chain_{i-1} || SHA256(document_i)),  chain_0 = 64 zeros (genesis)."""
import hashlib, glob

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

if __name__ == "__main__":
    files = sorted(glob.glob("pdfs/semester*_gradecard.pdf"))
    chain = "0" * 64
    print(f"Genesis hash: {chain}\n")
    for f in files:
        doc = sha256_file(f)
        chain = hashlib.sha256((chain + doc).encode()).hexdigest()
        print(f"Document : {f}\n  doc hash   : {doc}\n  chain hash : {chain}\n")
    print("Final hash of all documents:")
    print(chain)
