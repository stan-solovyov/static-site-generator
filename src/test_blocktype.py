import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("```Code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("- Unordered list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Ordered list"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("Paragraph"), BlockType.PARAGRAPH)