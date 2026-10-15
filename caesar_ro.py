# -*- coding: utf-8 -*-
"""
Laboratory Work No. 1 - Caesar cipher over the Romanian alphabet (n = 31)
Task 1.1: classic Caesar cipher (one numeric key)
Task 1.2: Caesar cipher with a keyword-permuted alphabet (two keys)

The shift is computed ONLY with the letter positions from Table 2
(no ASCII / Unicode code points are used for arithmetic).
"""

# Table 2: A=0, Ă=1, Â=2, ..., Z=30
ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "Ș", "T",
            "Ț", "U", "V", "W", "X", "Y", "Z"]
N = len(ALPHABET)  # 31

# Cedilla variants are treated as the same letters as the comma-below ones
VARIANTS = {"\u015E": "\u0218",  # Ş -> Ș
            "\u0162": "\u021A"}  # Ţ -> Ț

MIN_KEYWORD_LEN = 7


# ---------------------------------------------------------------- helpers
def normalize(text):
    """Uppercase, unify cedilla variants, remove spaces."""
    text = text.upper()
    text = "".join(VARIANTS.get(ch, ch) for ch in text)
    return text.replace(" ", "")


def first_invalid_char(text, alphabet):
    """Return the first character not in the alphabet, or None."""
    for ch in text:
        if ch not in alphabet:
            return ch
    return None


def build_index(alphabet):
    """letter -> position (dictionary lookup, no char codes)."""
    return {letter: i for i, letter in enumerate(alphabet)}


def build_permuted_alphabet(keyword):
    """Keyword letters (first occurrences only), then the remaining letters."""
    result = []
    for ch in keyword:
        if ch not in result:
            result.append(ch)
    for ch in ALPHABET:
        if ch not in result:
            result.append(ch)
    return result


# ----------------------------------------------------------------- cipher
def caesar(text, k, alphabet, decrypt=False):
    """text must already be normalized and valid."""
    index = build_index(alphabet)
    shift = -k if decrypt else k
    # Python's % is always non-negative for a positive modulus,
    # so (y - k) mod n is already in 0..n-1
    return "".join(alphabet[(index[ch] + shift) % N] for ch in text)


# ------------------------------------------------------------- input I/O
def ask_key():
    allowed = f"an integer from 1 to {N - 1}"
    while True:
        raw = input(f"Key k ({allowed}): ").strip()
        try:
            k = int(raw)
        except ValueError:
            print(f"  Invalid key '{raw}': the key must be {allowed}.")
            continue
        if 1 <= k <= N - 1:
            return k
        print(f"  Invalid key {k}: the key must be {allowed}.")


def ask_text(prompt):
    allowed = "Romanian letters (A-Z, Ă, Â, Î, Ș, Ț) and spaces"
    while True:
        text = normalize(input(prompt))
        bad = first_invalid_char(text, ALPHABET)
        if bad is not None:
            print(f"  Invalid character '{bad}'. Allowed: {allowed}.")
            continue
        if not text:
            print(f"  The text is empty. Enter {allowed}.")
            continue
        return text


def ask_keyword():
    while True:
        word = normalize(input(
            f"Keyword (Romanian letters only, at least {MIN_KEYWORD_LEN}): "))
        bad = first_invalid_char(word, ALPHABET)
        if bad is not None:
            print(f"  Invalid character '{bad}' in the keyword. "
                  f"Allowed: Romanian letters (A-Z, Ă, Â, Î, Ș, Ț).")
            continue
        if len(word) < MIN_KEYWORD_LEN:
            print(f"  Keyword too short ({len(word)} characters): "
                  f"at least {MIN_KEYWORD_LEN} are required.")
            continue
        return word


def ask_operation():
    while True:
        op = input("Operation: [e]ncrypt or [d]ecrypt? ").strip().lower()
        if op in ("e", "encrypt"):
            return False
        if op in ("d", "decrypt"):
            return True
        print("  Please enter 'e' (encrypt) or 'd' (decrypt).")


def run(task):
    decrypt = ask_operation()
    k = ask_key()
    alphabet = ALPHABET
    if task == 2:
        keyword = ask_keyword()
        alphabet = build_permuted_alphabet(keyword)
        print("Permuted alphabet:", " ".join(alphabet))
    text = ask_text("Ciphertext: " if decrypt else "Message: ")
    result = caesar(text, k, alphabet, decrypt)
    print("Decrypted message:" if decrypt else "Ciphertext:", result)


def main():
    while True:
        print("\n1) Caesar cipher (one key)\n"
              "2) Caesar cipher with permutation (two keys)\n"
              "0) Exit")
        choice = input("Choose task: ").strip()
        if choice == "1":
            run(1)
        elif choice == "2":
            run(2)
        elif choice == "0":
            break
        else:
            print("  Please enter 1, 2 or 0.")


if __name__ == "__main__":
    main()
