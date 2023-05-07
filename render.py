import os
import yaml
import json
import shutil
import htmlmin
import argparse
from datetime import datetime
from markdown import Markdown
from jinja2 import Environment, FileSystemLoader

SOURCE = os.path.join(os.path.dirname(__file__), "html")
TARGET = os.path.join(os.path.dirname(__file__), "dist")


def read_manifest() -> dict:
    with open(os.path.join(SOURCE, "manifest.yaml"), "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def main():
    arguments = parse_args()
    manifest = read_manifest()
    jinja_env = Environment(loader=FileSystemLoader(SOURCE))
    jinja_env.globals["now"] = datetime.now()
    jinja_env.globals["cdn"] = lambda base, url: url if url.startswith("http") else f"{arguments.cdn.rstrip('/')}/{base}{url.lstrip('/')}"

    print("Source:", SOURCE)
    print("Target:", TARGET)

    if arguments.clean:
        if os.path.exists(TARGET):
            print("Cleaning target directory:", TARGET)
            shutil.rmtree(TARGET)
        else:
            print("Target directory does not exist, cleaning skipped")

    for root, dirs, files in os.walk(SOURCE):
        for file in files:
            rel_dir = os.path.relpath(root, SOURCE).strip(".").strip("/")
            source_dir = os.path.join(SOURCE, rel_dir)
            target_dir = os.path.join(TARGET, rel_dir)
            source_path = os.path.join(source_dir, file)
            target_path = os.path.join(target_dir, file)
            os.makedirs(target_dir, exist_ok=True)

            if file.endswith(".html"):
                if file.startswith("_"):
                    print("Skipping rendering:", (rel_dir + "/" + file))
                    continue
                print("Rendering html:", (rel_dir + "/" + file))
                template = jinja_env.get_template((rel_dir + "/" + file).strip("/"))
                html = template.render(manifest)
                minified_html = htmlmin.minify(html, remove_comments=True, remove_empty_space=True)
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(minified_html)
                continue
            if file.endswith(".md"):
                print("Rendering markdown:", (rel_dir + "/" + file))
                with open(source_path, "r", encoding="utf-8") as f:
                    markdown = Markdown(extensions=["meta"])
                    content = markdown.convert(f.read())
                    metadata = markdown.Meta
                template = jinja_env.get_template((rel_dir + "/_markdown.html"))
                target_html_path = target_path[:-3] + ".html"
                html = template.render(manifest, markdown=content, metadata=metadata)
                minified_html = htmlmin.minify(html, remove_comments=True, remove_empty_space=True)
                with open(target_html_path, "w", encoding="utf-8") as f:
                    f.write(minified_html)
                continue
            shutil.copy(source_path, target_path)
    
    with open(os.path.join(TARGET, "manifest.json"), "w", encoding="utf-8") as f:
        print("Writing manifest.json")
        json.dump(manifest, f, ensure_ascii=False)
    print("Done")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE)
    parser.add_argument("--target", default=TARGET)
    parser.add_argument("--clean", action="store_true", default=False, help="Clean target directory before rendering")
    parser.add_argument("--cdn", default="assets")
    return parser.parse_args()


if __name__ == "__main__":
    main()
