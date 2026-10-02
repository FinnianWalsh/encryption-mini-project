import sys

from random import randint

lower_a_ord = ord('a')
upper_a_ord = ord('A')

lower_z_ord = ord('z')
upper_z_ord = ord('Z')

def get_number(prompt="") -> int:
    while 1:
        try:
            number = int(input(prompt))
            return number
            
        except BaseException as err:
            print(err, file=sys.stderr)
      

def letter_shift(ch, shift):
    num = ord(ch)

    if num >= lower_a_ord and num <= lower_z_ord:
        num = (num - lower_a_ord + shift) % 26 + lower_a_ord
    elif num >= upper_a_ord and num <= upper_z_ord:
         num = (num - upper_a_ord + shift) % 26 + upper_a_ord
    else:
        return ch

    return chr(num)

def printable_shift(ch, shift):
    if ch == " ":
        return chr(randint(32, 125))
    
    num = ord(ch) - 32
    assert num >= 0 and num <= 95, "Character must be printable ascii!"
    
    return chr((num + shift) % 95 + 32)

def caesar(text=None, shift=None, shift_fn=letter_shift):
    if text is None:
        text = input("Enter text: ")

    if shift is None:
        shift = get_number("Enter shift: ")
    
    buf = []
    
    for ch in text:
        buf.append(shift_fn(ch, shift))

    return "".join(buf)

def pad_num(n, digits):
    string = str(n)

    return "0" * (digits - len(string)) + string

def caesar_brute_decrypt():
    buf = []
    text = input("Enter text: ")
    
    for i in range(1, 26):
        buf.append(f"{pad_num(i, 2)}: {caesar(text, 26-i)}")

    return "\n".join(buf)

def into_printable_num(ch):
    num = ord(ch)
    assert num >= 32 and num <= 126, "Character must be a printable ascii character!"
    return num - 32

def xor_printable_chars(a, b):
    printable_ascii_num = into_printable_num(a) ^ into_printable_num(b)
    return chr(32 + printable_ascii_num)
    
def vernam(
    text=None,
    pad=None,
    char_xor=lambda a, b: chr(ord(a)^ord(b)),
):
    if text is None:
        text = input("Enter text: ")

    if pad is None:
        while 1:
            pad = input("Enter a pad: ")

            if len(pad) >= len(text):
                break

            print("The length of the pad must match the length of the text!", file=sys.stderr)
    
    assert len(pad) >= len(text), "The pad must be at least the length of the text!"
    buf = []

    for idx, ch in enumerate(text):
        buf.append(char_xor(ch, pad[idx]))

    return "".join(buf)

def encryption_help():
    return """\
Default caesar cipher:
Shifts letters by a fixed count

Caesar printable:
Caesar cipher that supports all 95 printable ascii characters
* since spaces would make the shift too obvious, they are randomised in the result

Caesar brute decrypt: print out all possible shifts of an encrypted message

Vernam cipher:
Use a one-time pad and a message to encrypt the message, fully reversible using the one-time pad.")

Vernam raw cipher:
Use a one-time pad to encrypt the message reversibly using exclusive or.
This vernam cipher is probably not as useful as the other one unless you
want to encrypt some non-ascii utf-8 characters"""


def capitalize(item):
    if len(item) == 0:
        return ""

    if len(item) == 1:
        return item[0].upper()

    return f"{item[0].upper()}{item[1:]}"

def name_of_function(f):
    return " ".join(map(capitalize, f.__name__.split("_")))

def handle_opt_arg(arg) -> str:
    if callable(arg):
        arg = (arg,)
        
    if isinstance(arg, tuple):
        assert len(arg) >= 1 and len(arg) <= 3, "Argument must be a tuple of length 1 to 3"

        function = arg[0]

        if len(arg) < 3:
            if len(arg) == 1:
                name = name_of_function(function)
                shorthand = function.__name__[0] if len(function.__name__) > 0 else "_"
            else:
                name = arg[1]
                shorthand = name[0].lower() if len(name) > 0 else "_"
        else:
            name, shorthand = arg[1] or name_of_function(function), arg[2]

        return (function, name, shorthand)
    else:
        print(type(arg))
        raise TypeError("Argument must be either a tuple or callable")

def select_from_opts(*args):
    items = [handle_opt_arg(arg) for arg in args]
    buf = [f"{idx}. {item[1]} ({item[2]})" for idx, item in enumerate(items)]

    print("\n".join(buf))

    response = input()

    if response.isdigit():
        return items[int(response)][0]()

    long_matches = []

    for item in items:
        if item[2] == response:
            return item[0]()
        elif item[1].startswith(response):
            long_matches.append(item)

    if len(long_matches) == 0:
        print("Invalid option", file=sys.stderr)        
    elif len(long_matches) == 1:
        return long_matches[0][0]()
    else:
        min(long_matches, key=lambda i: len(i[1]))[0]()

menu_options = (
    caesar,
    (lambda: caesar(shift_fn=printable_shift), "Caesar Printable", "cp"),
    (caesar_brute_decrypt, None, "b"),
    (lambda: vernam(char_xor=xor_printable_chars), "Vernam"),
    (vernam, "Vernam Raw", "r"),
    (encryption_help, "help", "h"),
)

while 1:
    print("Which method of encryption would you like to use?")

    print(select_from_opts(*menu_options), "\n")

