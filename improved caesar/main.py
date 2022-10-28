from dataclasses import dataclass


@dataclass
class Key:
    caesar: int
    jumps: int


def caesar_encrypt(word: str, key: Key) -> str:
    min_val = 32
    max_val = 126
    ascii_range = max_val-min_val
    extra: int = 0
    encrypted: str = ""
    for letter in word:
        new = (ord(letter) + key.caesar + extra -
               min_val) % ascii_range + min_val
        encrypted += chr(new)
        extra += key.jumps

    return encrypted


def caesar_decrypt(word: str, key: Key) -> str:
    min_val = 32
    max_val = 126
    ascii_range = max_val - min_val
    extra = 0
    decrypted: str = ""
    for letter in word:
        new = (ord(letter) - key.caesar - extra -
               min_val) % ascii_range + min_val
        # if (ord(letter) - extra - key.caesar) < min_val:
        #     new = max_val - \
        #         (abs(min_val-1 - (ord(letter) - extra - key.caesar)) % (ascii_range))
        # else:
        #     new = (ord(letter) - extra - key.caesar)
        decrypted += chr(new)
        extra += key.jumps

    return decrypted


def main() -> None:
    key = Key(caesar=0, jumps=1)
    # word = "Hello World!"
    word = "0123456789"

    encrypted = caesar_encrypt(word, key)

    print(encrypted)

    decrypted = caesar_decrypt(encrypted, key)

    # for i in range(len(encrypted)):
    #     print(f"{chr(ord(encrypted[i]) - key.jumps*i)}, {key.jumps*i}")

    print(decrypted)


if __name__ == '__main__':
    main()
