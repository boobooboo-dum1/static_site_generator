from pathlib import Path

from jinja2 import Template

from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found")


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    print(
        f"Generating page from {str(from_path)} to {str(dest_path)} using {str(template_path)}"
    )

    markdown = from_path.read_text()
    template = Template(template_path.read_text())
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    title = extract_title(markdown)

    templated = template.render(Title=title, Content=html_content)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with dest_path.open("w", encoding="utf-8") as f:
        f.write(templated)
