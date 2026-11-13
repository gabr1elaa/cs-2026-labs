# Laboratory work 4 - Block ciphers. The DES algorithm
# Task 2.7 (n = 7, 7 mod 11 = 7)
# Given B1 B2 B3 B4 B5 B6 B7 B8 (48 bits), find
# S1(B1) S2(B2) S3(B3) S4(B4) S5(B5) S6(B6) S7(B7) S8(B8) (32 bits)

import random

# the 8 S-boxes of DES (FIPS 46-3), each one has 4 rows and 16 columns
S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
]


def print_sbox(number):
    """Prints one S-box as a table with the numbers of rows and columns."""
    box = S_BOXES[number - 1]
    print("S" + str(number))
    header = "row\\col |"
    for col in range(16):
        header += str(col).rjust(3)
    print(header)
    print("-" * len(header))
    for row in range(4):
        line = str(row).center(7) + " |"
        for col in range(16):
            line += str(box[row][col]).rjust(3)
        print(line)
    print()


def print_all_sboxes():
    print("=" * 57)
    print("The S-boxes used by the DES algorithm")
    print("=" * 57)
    for i in range(1, 9):
        print_sbox(i)


def read_bits():
    """Reads the 48 bits from the keyboard (binary or hexadecimal)."""
    while True:
        text = input("Enter B1...B8 (48 bits or 12 hex digits): ")
        # the user can write the blocks with spaces between them
        text = text.replace(" ", "").upper()
        if len(text) == 48:
            ok = True
            for ch in text:
                if ch != "0" and ch != "1":
                    ok = False
            if ok:
                return text
            print("Error: a binary input must contain only 0 and 1.")
        elif len(text) == 12:
            ok = True
            for ch in text:
                if ch not in "0123456789ABCDEF":
                    ok = False
            if ok:
                # every hex digit gives 4 bits
                bits = ""
                for ch in text:
                    bits += bin(int(ch, 16))[2:].zfill(4)
                print("In binary:", bits)
                return bits
            print("Error: a hex input must contain only 0-9 and A-F.")
        else:
            print("Error: I need exactly 48 bits or 12 hex digits,"
                  " you entered " + str(len(text)) + " characters.")


def random_bits():
    """Generates 48 random bits."""
    bits = ""
    for i in range(48):
        bits += str(random.randint(0, 1))
    return bits


def split_blocks(bits):
    """Splits the 48 bits into 8 blocks of 6 bits."""
    blocks = []
    for i in range(0, 48, 6):
        blocks.append(bits[i:i + 6])
    return blocks


def sbox_step(number, block):
    """Applies the S-box with the given number to a block of 6 bits.
    Prints all the steps and returns the 4 bits of the result."""
    # first and last bit give the row
    row_bits = block[0] + block[5]
    # the 4 bits from the middle give the column
    col_bits = block[1:5]
    row = int(row_bits, 2)
    col = int(col_bits, 2)

    value = S_BOXES[number - 1][row][col]
    result = bin(value)[2:].zfill(4)

    print("B" + str(number) + " = " + block)
    print("   row    = first and last bit = " + row_bits + " = " + str(row))
    print("   column = the 4 middle bits  = " + col_bits + " = " + str(col))
    print("   S" + str(number) + "[" + str(row) + "][" + str(col) + "] = "
          + str(value) + " = " + result)
    print("   S" + str(number) + "(B" + str(number) + ") = " + result)
    print()
    return result


def solve(bits):
    blocks = split_blocks(bits)
    print("=" * 57)
    print("Step 1. Split the 48 bits into 8 blocks of 6 bits")
    print("=" * 57)
    print("Input = " + bits)
    for i in range(8):
        print("B" + str(i + 1) + " = " + blocks[i])
    print("B1 B2 B3 B4 B5 B6 B7 B8 = " + " ".join(blocks))
    print()
    print("=" * 57)
    print("Step 2. Apply the S-box Si to every block Bi")
    print("=" * 57)
    results = []
    for i in range(8):
        results.append(sbox_step(i + 1, blocks[i]))
    print("=" * 57)
    print("Step 3. Summary")
    print("=" * 57)
    print(" i |   Bi   | row | column | Si value | Si(Bi)")
    print("---+--------+-----+--------+----------+-------")
    for i in range(8):
        b = blocks[i]
        row = int(b[0] + b[5], 2)
        col = int(b[1:5], 2)
        print(" " + str(i + 1) + " | " + b + " | " + str(row).center(3) + " | "
              + str(col).center(6) + " | " + str(int(results[i], 2)).center(8)
              + " | " + results[i])
    print()
    final = "".join(results)
    print("=" * 57)
    print("Result")
    print("=" * 57)
    print("S1(B1)S2(B2)S3(B3)S4(B4)S5(B5)S6(B6)S7(B7)S8(B8) =")
    print("= " + " ".join(results))
    print("= " + final + " (32 bits)")
    print("= " + hex(int(final, 2))[2:].upper().zfill(8) + " (hex)")
    print()


def main():
    print("DES algorithm - task 2.7")
    print("Given B1B2B3B4B5B6B7B8, find S1(B1)S2(B2)...S8(B8)")
    while True:
        print()
        print("1 - enter B1...B8 from the keyboard")
        print("2 - generate B1...B8 randomly")
        print("3 - show the S-boxes")
        print("0 - exit")
        option = input("Your option: ").strip()

        if option == "1":
            bits = read_bits()
        elif option == "2":
            bits = random_bits()
            print("Generated bits: " + bits)
        elif option == "3":
            print_all_sboxes()
            continue
        elif option == "0":
            print("Bye!")
            break
        else:
            print("Error: choose 0, 1, 2 or 3.")
            continue

        print()
        print_all_sboxes()
        solve(bits)


if __name__ == "__main__":
    main()
