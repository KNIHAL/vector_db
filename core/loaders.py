from pypdf import PdfReader
import markdown
import re

def load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        if page.extract_text():
            text.append(page.extract_text())
    return "\n".join(text)

def load_md(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        md_text = f.read()
    html = markdown.markdown(md_text)
    return re.sub("<[^<]+?>", "", html)  # strip HTML
