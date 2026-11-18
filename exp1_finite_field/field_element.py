class FieldElement:
    """An element of the finite field F_p (p prime)."""

    def __init__(self, num, prime):
        if num < 0 or num >= prime:
            raise ValueError(f"Num {num} not in field range 0 to {prime - 1}")
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f"FieldElement_{self.prime}({self.num})"

    def __eq__(self, other):
        if not isinstance(other, FieldElement):
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not (self == other)

    def _check(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot operate on two numbers in different Fields")

    def __add__(self, other):
        self._check(other)
        return FieldElement((self.num + other.num) % self.prime, self.prime)

    def __sub__(self, other):
        self._check(other)
        return FieldElement((self.num - other.num) % self.prime, self.prime)

    def __mul__(self, other):
        self._check(other)
        return FieldElement((self.num * other.num) % self.prime, self.prime)


if __name__ == "__main__":
    p = 31
    a, b, c = FieldElement(2, p), FieldElement(15, p), FieldElement(2, p)
    print("a =", a, "| b =", b, "| c =", c)
    print("\n-- Equality --")
    print("a == c :", a == c)
    print("a == b :", a == b)
    print("a != b :", a != b)
    print("a == FieldElement(2, 17) :", a == FieldElement(2, 17))
    print("\n-- Arithmetic in F_31 --")
    print("a + b =", a + b, " (2 + 15 = 17)")
    print("a - b =", a - b, " (2 - 15 = -13 mod 31 = 18)")
    print("a * b =", a * b, " (2 * 15 = 30)")
    x, y = FieldElement(24, p), FieldElement(19, p)
    print("24 + 19 =", x + y, " (43 mod 31 = 12)")
    print("24 * 19 =", x * y, " (456 mod 31 = 22)")
    print("\n-- Invalid element --")
    for n, pr in [(31, 31), (-1, 31)]:
        try:
            FieldElement(n, pr)
        except ValueError as e:
            print(f"FieldElement({n}, {pr}) -> ValueError: {e}")
    print("\n-- Different fields --")
    try:
        a + FieldElement(2, 17)
    except TypeError as e:
        print("TypeError:", e)
