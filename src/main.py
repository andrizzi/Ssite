import os
import shutil

from Generate import generate_pages_recursive
from copystatic import copy_files_recursive


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # Generate a page from content/index.md using template.html and write it to public/index.html.
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )


main()
