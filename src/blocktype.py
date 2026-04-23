from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"\d+\. ", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH