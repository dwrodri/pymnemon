from typing import List, Dict
from random import choice
from string import Template


def load_list(filename: str) -> List[str]:
    """
    Reads a wordlist from disk
    """
    with open(filename, "r") as fp:
        return [line.strip() for line in fp.readlines()]


ADJECTIVES: List[str] = load_list("adjectives.txt")
NOUNS: List[str] = load_list("nouns.txt")
WORDLIST_LOOKUP: Dict[str, List[str]] = {"${ADJ}": ADJECTIVES, "${N}": NOUNS}


def replace_range(new_content: str, target: str, start: int, end: int) -> str:
    """
    Replace `target[start:end]` with `new_content`.
    """
    if start > len(target):
        raise IndexError(
            f"start index {start} is too large for target string with length {len(target)}"
        )

    return target[:start] + new_content + target[end + 1 :]


class RandomTagGenerator:
    def __init__(self, format_str: Template = Template("${ADJ}_${N}")) -> None:
        self.format_str = format_str
        self.counter = 0

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self) -> str:
        temp: str = self.format_str.template
        for match in self.format_str.pattern.finditer(self.format_str.template):
            temp = replace_range(
                choice(WORDLIST_LOOKUP[match.group()]), temp, *match.span()
            )
        return temp


if __name__ == "__main__":
    for _ in range(10):
        for tag in RandomTagGenerator():
            print(tag)
