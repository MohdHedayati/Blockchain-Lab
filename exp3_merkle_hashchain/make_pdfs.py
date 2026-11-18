"""Generates 4 made-up semester grade-card PDFs (minimal hand-written PDF, no libraries)."""
import os, random

random.seed(7)
SUBJECTS = {
    1: ["Engineering Maths I", "Physics", "Basic Electronics", "C Programming", "Communication Skills"],
    2: ["Engineering Maths II", "Data Structures", "Digital Logic", "Chemistry", "Object Oriented Prog"],
    3: ["Discrete Maths", "Computer Organization", "Database Systems", "Algorithms", "Operating Systems"],
    4: ["Computer Networks", "Theory of Computation", "Software Engineering", "Cryptography", "Web Technologies"],
}
GRADES = ["AA", "AB", "BB", "BC", "CC"]


def make_pdf(path, lines):
    content = "BT /F1 12 Tf 50 780 Td 16 TL\n" + "\n".join(
        f"({l.replace('(', '[').replace(')', ']')}) '" for l in lines) + "\nET"
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
        "/Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n"
    out += "".join(f"{o:010d} 00000 n \n" for o in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    with open(path, "wb") as f:
        f.write(out.encode("latin-1"))


os.makedirs("pdfs", exist_ok=True)
for sem in range(1, 5):
    lines = ["Veermata Jijabai Technological Institute", f"Grade Card - Semester {sem}",
             "Student: Reg ID 241080023", ""]
    lines += [f"{s}: {random.choice(GRADES)}" for s in SUBJECTS[sem]]
    make_pdf(f"pdfs/semester{sem}_gradecard.pdf", lines)
    print("created", f"pdfs/semester{sem}_gradecard.pdf")
