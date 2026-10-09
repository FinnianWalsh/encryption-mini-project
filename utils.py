import sys

from typing import Callable, Union, List

AnyFunction = Callable[..., object]

class Option:
    def __init__(
        self,
        func: AnyFunction,
        name: Union[str, None] = None,
        shorthand: Union[str, None] = None,
    ):
        if name is None:
            split_name = func.__name__.split("_")

            if shorthand is None:
                shorthand = "".join(
                    word[0] if len(word) >= 1 else "" for word in split_name
                )

            name = " ".join(map(str.capitalize, split_name))
        elif shorthand is None:
            shorthand = "".join(
                word[0].lower() if len(word) >= 1 else "" for word in name.split(" ")
            )

        self.func = func
        self.name = name
        self.shorthand = shorthand
        self.help_str = "not documented"

    def __call__(self) -> object:
        return self.func()

    def __str__(self) -> str:
        return f"{self.name} ({self.shorthand})"

    def set_help(self, help_str: str):
        self.help_str = help_str
        return self

    def help(self) -> str:
        return f"{self.name}\n{self.help_str}"


def select_option(options: List[Option]) -> object:
    print(
        "\n".join([f"{idx}. {option}" for idx, option in enumerate(options, start=1)])
    )

    response = input()

    if response.isdigit():
        if response == "0":
            print("\n".join(opt.help() for opt in options))
        index = int(response) - 1
        assert 0 <= index and index < len(options), (
            f"Index must be within range of options (0 to {len(options)})"
        )
        return options[index]()

    full_name_match = None

    for option in options:
        if option.shorthand == response:
            return option()
        elif option.name.startswith(response):
            if not full_name_match:
                full_name_match = option
                continue

            if len(full_name_match.name) > len(option.name):
                full_name_match = option

    if full_name_match:
        return full_name_match()
    else:
        print("Invalid option", file=sys.stderr)

if __name__ == "__main__":
    print("Options test!")

    options = [
        Option(print),
        Option(input),
    ]

    print("Got:", select_option(options))
