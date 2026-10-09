import sys

from random import randint
from typing import Callable, List, Union

from utils import Option, select_option

Cipher = Callable[[], object]

LOWER_A_ORD = ord("a")
UPPER_A_ORD = ord("A")

LOWER_Z_ORD = ord("z")
UPPER_Z_ORD = ord("Z")


def get_number(prompt: str = "") -> int:
    while True:
        try:
            number = int(input(prompt))
            return number

        except BaseException as err:
            print(err, file=sys.stderr)


def letter_shift(ch: str, shift: int):
    num = ord(ch)

    if num >= LOWER_A_ORD and num <= LOWER_Z_ORD:
        num = (num - LOWER_A_ORD + shift) % 26 + LOWER_A_ORD
    elif num >= UPPER_A_ORD and num <= UPPER_Z_ORD:
        num = (num - UPPER_A_ORD + shift) % 26 + UPPER_A_ORD
    else:
        return ch

    return chr(num)


def printable_shift(ch: str, shift: int):
    if ch == " ":
        return chr(randint(32, 125))

    num = ord(ch) - 32
    assert num >= 0 and num <= 95, "Character must be printable ascii!"

    return chr((num + shift) % 95 + 32)


def caesar(
    text: Union[str, None] = None,
    shift: Union[int, None] = None,
    shift_method: Callable[[str, int], str] = letter_shift,
):
    if text is None:
        text = input("Enter text: ")

    if shift is None:
        shift = get_number("Enter shift: ")

    buf: List[str] = []

    for ch in text:
        buf.append(shift_method(ch, shift))

    return "".join(buf)


def pad_num(n: int, digits: int) -> str:
    string = str(n)

    return f"{'0' * (digits - len(string))}{string}"


def caesar_brute_decrypt():
    buf: List[str] = []
    text = input("Enter text: ")

    for i in range(1, 26):
        buf.append(f"{pad_num(i, 2)}: {caesar(text, 26 - i)}")

    return "\n".join(buf)


def into_printable_num(ch: str):
    num = ord(ch)
    assert num >= 32 and num <= 126, "Character must be a printable ascii character!"
    return num - 32


def xor_printable_chars(a: str, b: str):
    printable_ascii_num = into_printable_num(a) ^ into_printable_num(b)
    return chr(32 + printable_ascii_num)


def vernam(
    text: Union[str, None] = None,
    pad: Union[str, None] = None,
    char_xor: Callable[[str, str], str] = lambda a, b: chr(ord(a) ^ ord(b)),
):
    if text is None:
        text = input("Enter text: ")

    if pad is None:
        while True:
            pad = input("Enter a pad: ")

            if len(pad) >= len(text):
                break

            print(
                "The length of the pad must match the length of the text!",
                file=sys.stderr,
            )

    assert len(pad) >= len(text), "The pad must be at least the length of the text!"
    buf: List[str] = []

    for idx, ch in enumerate(text):
        buf.append(char_xor(ch, pad[idx]))

    return "".join(buf)



menu_options = [
    Option(caesar).set_help("Shifts letters by a fixed count"),
    Option(lambda: caesar(shift_method=printable_shift), "Caesar Printable").set_help(
        """Caesar cipher that supports all 95 printable ascii characters
* since spaces would make the shift too obvious, they are randomised in the result"""
    ),
    Option(caesar_brute_decrypt, None, "b").set_help(
        "Print out all possible caesar cipher shifts of an encrypted message"
    ),
    Option(lambda: vernam(char_xor=xor_printable_chars), "Vernam").set_help(
        "Use a one-time pad and a message to encrypt the message, fully reversible using the one-time pad."
    ),
    Option(
        vernam, "Vernam Raw"
    ).set_help("""Use a one-time pad to encrypt the message reversibly using exclusive or.
This vernam cipher is probably not as useful as the other one unless you
want to encrypt some non-ascii utf-8 characters"""),
    Option(lambda: "\n\n".join(opt.help() for opt in menu_options), "help").set_help(
        "Get help"
    ),
]


if __name__ == "__main__":
    while True:
        print("Which method of encryption would you like to use?")
        print(select_option(menu_options), "\n")
