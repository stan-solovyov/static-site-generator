from blocktype import BlockType, block_to_block_type
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType
import re


def normalize_basepath(basepath):
    if not basepath or basepath == "/":
        return ""
    normalized = basepath if basepath.startswith("/") else f"/{basepath}"
    return normalized.rstrip("/")


def text_node_to_html_node(text_node, basepath="/"):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            count = node.text.count(delimiter)
            if count % 2:
                raise Exception(f"Invalid markdown syntax")
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                parts = re.split(r"!\[[^\[\]]*\]\([^\(\)]*\)", node.text)
                for i, part in enumerate(parts):
                    if part != "":
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    if i < len(matches):
                        alt_text, url = matches[i]
                        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_links(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                parts = re.split(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", node.text)
                for i, part in enumerate(parts):
                    if part != "":
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    if i < len(matches):
                        link_text, url = matches[i]
                        new_nodes.append(TextNode(link_text, TextType.LINK, url))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    node = split_nodes_delimiter([node], "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if line.strip() == "":
            continue
        blocks.append(line.strip())
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.HEADING:
            h_count = len(block) - len(block.lstrip('#'))
            children = text_to_children(block[h_count+1:].strip())
            html_nodes.append(ParentNode (f'h{h_count}', children))
        elif blocktype == BlockType.QUOTE:
            b = block.split("\n")
            for i in range(len(b)):
                b[i] = b[i][2:].strip()
            html_nodes.append(ParentNode('blockquote', text_to_children("\n".join(b))))
        elif blocktype == BlockType.CODE:
            code_text = block[4:-3]
            text_node = TextNode(code_text, TextType.TEXT)
            code_leaf = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [code_leaf])
            pre_node = ParentNode("pre", [code_node])
            html_nodes.append(pre_node)
        elif blocktype == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            ul_node = ParentNode('ul', [])
            for item in items:
                children = text_to_children(item[2:].strip())
                li_node = ParentNode('li', children)
                ul_node.children.append(li_node)
            html_nodes.append(ul_node)
        elif blocktype == BlockType.ORDERED_LIST:
            items = block.split("\n")
            ol_node = ParentNode('ol', [])
            for item in items:
                children = text_to_children(re.sub(r"^\d+\. ", "", item).strip())
                li_node = ParentNode('li', children)
                ol_node.children.append(li_node)
            html_nodes.append(ol_node)
        else:
            textnodes = text_to_children(block.replace("\n", " "))
            p_node = ParentNode('p', textnodes)
            html_nodes.append(p_node)
    parent_node = ParentNode('div', [])
    parent_node.children = html_nodes
    return parent_node

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    markdown_node = markdown_to_html_node(markdown)
    markdown_html = markdown_node.to_html()
    title = extract_title(markdown)
    page_html = template.replace("{{ Content }}", markdown_html).replace("{{ Title }}", title)
    page_html = page_html.replace("href=\"/", f"href=\"{basepath}")
    page_html = page_html.replace("src=\"/", f"src=\"{basepath}")
    page_html = page_html.replace("{{ Basepath }}", normalize_basepath(basepath))
    if not dest_path.parent.exists():
        dest_path.parent.mkdir(parents=True)
    with open(dest_path, "w") as f:
        f.write(page_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for item in dir_path_content.iterdir():
        if item.is_dir():
            generate_pages_recursive(item, template_path, dest_dir_path / item.name, basepath)
        elif item.suffix == ".md":
            dest_path = dest_dir_path / (item.stem + ".html")
            generate_page(item, template_path, dest_path, basepath)