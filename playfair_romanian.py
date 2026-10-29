
class PlayfairRomanian:
    ALPHABET = 'AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ'

    ROWS = 6
    COLS = 6

    FILLER = 'X'
    ALT_FILLER = 'Q'
    EMPTY = '*'

    def __init__(self, key):
        key = self.prepare_text(key)

        if len(key) < 7:
            raise ValueError("Cheia trebuie să aibă cel puțin 7 caractere.")

        self.matrix = self.build_matrix(key)

        self.position = {
            letter: (r, c)
            for r, row in enumerate(self.matrix)
            for c, letter in enumerate(row)
            if letter != self.EMPTY
        }

    # Normalizează textul și verifică alfabetul
    def prepare_text(self, text):
        text = ''.join(text.split()).upper()
        text = text.replace('Ş', 'Ș').replace('Ţ', 'Ț')
        for char in text:
            if char not in self.ALPHABET:
                raise ValueError(
                    f"Caracterul '{char}' nu aparține alfabetului românesc."
                )
        return text


    def build_matrix(self, key):
        letters = list(dict.fromkeys(key + self.ALPHABET))
        letters.extend([self.EMPTY] * (
            self.ROWS * self.COLS - len(letters)
        ))
        return [
            letters[i:i + self.COLS]
            for i in range(0, len(letters), self.COLS)
        ]


    def print_matrix(self):
        line = "─" * (self.COLS * 4 - 1)
        print("\nMatricea Playfair:")
        print(f"┌{line}┐")
        for row in self.matrix:
            print("│ " + " │ ".join(row) + " │")

        print(f"└{line}┘")

    def filler_for(self, letter):
        return self.ALT_FILLER if letter == self.FILLER else self.FILLER

    def make_pairs(self, text):
        pairs = []
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 == len(text):
                b = self.filler_for(a)
                i += 1
            elif text[i + 1] == a:
                b = self.filler_for(a)
                i += 1
            else:
                b = text[i + 1]
                i += 2
            pairs.append((a, b))
        return pairs

    # Deplasează poziția până la următoarea literă validă
    # Ignoră pozițiile marcate cu '*'
    def shift_position(self, r, c, step, direction):
        for _ in range(1, 7):
            if direction == 'row':
                c = (c + step) % self.COLS
            else:
                r = (r + step) % self.ROWS
            if self.matrix[r][c] != self.EMPTY:
                return r, c
        raise RuntimeError("Nu există poziție validă în matrice.")

    def transform_pair(self, a, b, step):
        r1, c1 = self.position[a]
        r2, c2 = self.position[b]
        # Cazul 1: caracterele se află pe aceeași linie
        if r1 == r2:
            nr1, nc1 = self.shift_position( r1, c1, step, 'row')
            nr2, nc2 = self.shift_position(r2, c2, step, 'row')
            return (self.matrix[nr1][nc1], self.matrix[nr2][nc2])
        # Cazul 2: caracterele se află pe aceeași coloană
        if c1 == c2:
            nr1, nc1 = self.shift_position(r1, c1, step, 'column')
            nr2, nc2 = self.shift_position(r2, c2, step, 'column')
            return (self.matrix[nr1][nc1], self.matrix[nr2][nc2])
        # Cazul 3: caracterele formează un dreptunghi
        return (self.matrix[r1][c2], self.matrix[r2][c1])

    def encrypt(self, plaintext):
        text = self.prepare_text(plaintext)
        pairs = self.make_pairs(text)
        return ''.join(a + b
            for a, b in (
                self.transform_pair(x, y, +1)
                for x, y in pairs
            )
        )

    def decrypt(self, ciphertext):
        text = self.prepare_text(ciphertext)
        if len(text) % 2 != 0:
            raise ValueError(
                "Criptograma trebuie să aibă un număr par de litere."
            )
        pairs = zip(text[0::2], text[1::2])
        return ''.join(a + b
            for a, b in (
                self.transform_pair(x, y, -1)
                for x, y in pairs
            )
        )


VALID_LETTERS = set(
    PlayfairRomanian.ALPHABET
    + PlayfairRomanian.ALPHABET.lower()
    + 'ŞŢşţ'
)
RANGE_HINT = (
    "Sunt permise doar literele A-Z și a-z, "
    "plus Ă, Â, Î, Ș, Ț (mari sau mici)."
)
# Verifică dacă textul conține doar caractere permise
def check_letters(text):
    for char in text:
        if char not in VALID_LETTERS:
            return f"Caracterul '{char}' nu este permis. {RANGE_HINT}"
    return None
def check_key(key):
    key = ''.join(key.split())

    if len(key) < 7:
        return "Cheia trebuie să aibă cel puțin 7 caractere."

    return check_letters(key)
def check_message(text):
    text = ''.join(text.split())

    if not text:
        return "Mesajul nu poate fi gol."

    return check_letters(text)
# Verifică criptograma
def check_ciphertext(text):
    text = ''.join(text.split())

    if not text:
        return "Criptograma nu poate fi goală."

    if len(text) % 2 != 0:
        return "Criptograma trebuie să aibă un număr par de litere."

    return check_letters(text)

# Solicită o valoare până când aceasta este validă
def ask(prompt, check):
    while True:
        value = input(prompt).strip()
        error = check(value)
        if error is None:
            return value
        print("Eroare:", error)
# Modul de criptare
def encrypt_mode():
    key = ask("\nCheia (minim 7 litere): ", check_key)
    playfair = PlayfairRomanian(key)
    playfair.print_matrix()
    message = ask("\nMesajul de criptat: ", check_message)
    print("\nCriptograma:", playfair.encrypt(message))
    print("Spațiile se adaugă manual, după sensul mesajului.")

# Modul de decriptare
def decrypt_mode():
    key = ask("\nCheia (minim 7 litere): ", check_key)
    playfair = PlayfairRomanian(key)
    playfair.print_matrix()
    ciphertext = ask("\nCriptograma: ", check_ciphertext)
    print("\nMesajul decriptat:", playfair.decrypt(ciphertext))
    print(
        "Elimină manual literele X sau Q adăugate la criptare,"
    )
    print(
        "restabilește eventualele litere J în loc de I "
        "doar dacă este cazul și adaugă spațiile."
    )


def main():
    print("Cifrul Playfair - alfabetul românesc")

    while True:
        print("\n1. Criptare")
        print("2. Decriptare")
        print("0. Ieșire")

        choice = input("Alege: ").strip()

        if choice == '1':
            encrypt_mode()

        elif choice == '2':
            decrypt_mode()

        elif choice == '0':
            print("Program încheiat.")
            break

        else:
            print("Alege 1, 2 sau 0.")


if __name__ == "__main__":
    main()
