"""
Streamlit st.html() format: "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>" 
"""

import pathlib
import pymupdf4llm
md = pymupdf4llm.to_markdown("test.pdf")
pathlib.Path("output.md").write_bytes(md.encode())


"""
import fitz

docs = fitz.open("test.pdf")
page = docs[0]
words = page.get_text("words", sort=True)

for i, group in enumerate(words):
    word = group[4]
    print(word)
    pass
"""