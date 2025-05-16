import re
from htmlnode import *
from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    """
    Extracts markdown links from the given text.

    :param text: The input text containing markdown links.
    :return: A list of tuples containing the link text and URL.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes
    

def text_to_textnodes(text):
    #Just use all your splitting functions one after the other.
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    return nodes


def markdown_to_blocks(markdown):
    """
    Convert markdown text to a list of TextNode objects.

    :param markdown: The input markdown text.
    :return: A list of TextNode objects representing the parsed markdown.
    """
    # Split the markdown into lines
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if line == "":
            continue
        line = line.strip()
        blocks.append(line.strip("\n"))
    return blocks

def block_to_block_type(block):
    """
    Convert a block of text to its corresponding block type.

    :param block: The input block of text.
    :return: The block type as a BlockType enum value.
    """
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("-"):# or block.startswith("*"):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1."):#re.match(r"^\d+\.", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text):
    """
    Convert a block of text to its corresponding children nodes using functions from the textnode module and above
    :param text: The input block of text.
    :return: A list of child nodes representing the parsed text.
    """
    text = text.strip("\n")
    text = text.replace("\n", " ")
    # First convert text to TextNode objects (handling inline markdown)
    text_nodes = text_to_textnodes(text)
    
    # Then convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
        
    return html_nodes

    
def markdown_to_html_node(markdown):
    """
    we're going to use all the functions above to convert a markdown string to an HTMLNode
    """
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            nodes.append(ParentNode(tag="p", children=text_to_children(block)))
        elif block_type == BlockType.HEADING:
            # Determine heading level by counting #
            level = 1
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            level = min(level, 6)  # Max heading level is h6
            # Remove the # characters and process the rest
            text = block.lstrip('#').strip()
            nodes.append(ParentNode(tag=f"h{level}", children=text_to_children(text)))
        elif block_type == BlockType.CODE:
            # For code blocks, don't process inline markdown
            # Remove the ``` markers and get the content
            content = block.strip('`').strip()
            text_node = TextNode(content, TextType.CODE_TEXT)
            html_node = text_node_to_html_node(text_node)
            nodes.append(ParentNode(tag="pre", children=[html_node]))
        elif block_type == BlockType.QUOTE:
            # For quotes, remove the > marker and process the rest
            text = block.lstrip('>').strip()
            nodes.append(ParentNode(tag="blockquote", children=text_to_children(text)))
        elif block_type == BlockType.UNORDERED_LIST:
            # For unordered lists, remove the - marker and process the rest
            items = block.split("\n")
            list_items = []
            for item in items:
                item = item.lstrip('-').strip()
                if item:
                    list_items.append(ParentNode(tag="li", children=text_to_children(item)))
            nodes.append(ParentNode(tag="ul", children=list_items))
        elif block_type == BlockType.ORDERED_LIST:
            # For ordered lists, remove the number and dot and process the rest
            items = block.split("\n")
            list_items = []
            for item in items:
                item = re.sub(r"^\d+\.\s*", "", item).strip()
                if item:
                    list_items.append(ParentNode(tag="li", children=text_to_children(item)))
            nodes.append(ParentNode(tag="ol", children=list_items))
        else:
            # For any other type of block, treat it as a paragraph
            nodes.append(ParentNode(tag="p", children=text_to_children(block)))
    # Return the root node containing all the blocks
    return ParentNode(tag="div", children=nodes)


def extract_title(markdown):
    """
    Extract the title from the markdown text.
    The title is assumed to be the first heading (h1) in the markdown.
    """
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        line = block.strip("\n").split("\n")[0]
        if line.startswith("#"):
            return line.strip("#").strip()
    return None