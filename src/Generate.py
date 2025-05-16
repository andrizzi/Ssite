import os
from pathlib import Path
from ExMarkLink import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):

    print(f" Generating page from {from_path} to -> {dest_path} using {template_path}")
    """
    Read the markdown file at from_path and store the contents in a variable.
    Read the template file at template_path and store the contents in a variable."""
    f = open(from_path)
    markdown = f.read()
    f.close()
    
    f =  open(template_path)
    template = f.read()
    f.close()

    """
    Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    Use the extract_title function to grab the title of the page.
    """
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)
    """
    Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    """
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)    
    #close files

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Crawl every entry in the content directory
    For each markdown file found, generate a new .html file using the same template.html. 
    The generated pages should be written to the public directory in the same directory structure.
    """
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
