import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block]
    return blocks


def block_to_block_type(markdomn_block: str) -> str:
    def ordered_list_validator(text: str):
        lines = text.split("\n")

        if not re.match(r"^\d+\.{1}\s+.*$", lines[0]):
            return False
        base_number = int(lines[0].split(".", maxsplit=1)[0])
        for cur_number, line in enumerate(lines[1:], start=base_number + 1):
            pattern = rf"^{cur_number}\.{{1}}\s+.*$"
            if not re.match(pattern, line):
                return False
        return True

    validators_func = {
        BlockType.HEADING: lambda x: bool(re.match(r"^#{1,6}\s+.*$", x)),
        BlockType.CODE: lambda x: bool(re.match(r"^`{3}(.|\n)*`{3}$", x)),
        BlockType.QUOTE: lambda x: all(
            [bool(re.match(r"^>+.*$", line)) for line in x.split("\n")]
        ),
        BlockType.UNORDERED_LIST: lambda x: all(
            [bool(re.match(r"^(\*|-){1}\s+.*$", line)) for line in x.split("\n")]
        ),
        BlockType.ORDERED_LIST: ordered_list_validator,
    }

    for block_type, validator_func in validators_func.items():
        if validator_func(markdomn_block):
            return block_type.value

    return BlockType.PARAGRAPH.value
