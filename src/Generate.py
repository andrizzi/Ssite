import os
import shutil
from ExMarkLink import markdown_to_html_node, extract_title
from htmlnode import *

def generate_pages(from_path, template_path, dest_path):

    print(f" Generating page from {from_path} to -> {dest_path} using {template_path}")
    """
    Read the markdown file at from_path and store the contents in a variable.
    Read the template file at template_path and store the contents in a variable."""
    with open(from_path) as f:
        markdown = f.read()
    f.close()
    with open(template_path) as f:
        template = f.read()

    """
    Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    Use the extract_title function to grab the title of the page.
    """
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = node.extract_title()
    """
    Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    """
    template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)    
    #close files
    f.close()
    