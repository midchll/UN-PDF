import streamlit as st
from parser import Parser
import tempfile
import markdown

st.title("UN-PDF")
st.header("From PDF..")
st.subheader("To Markdown and HTML")

input_file = st.file_uploader("Your PDF:", type="pdf")

if input_file:
    # Temporarily save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(input_file.read())
        temp_pdf_path = temp_file.name
        
    parser = Parser(temp_pdf_path)
    
    md_cont = parser.parse_markdown()
    md_raw = md_cont.encode()
    html = markdown.markdown("## text string")

    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = parser.extract_images(temp_dir)

    markdown, html = st.tabs(["Markdown", "HTML"])

    with markdown:
        options = ["preview", "raw", "images"]
            
        selection = st.segmented_control(
            "Markdown Views", options, selection_mode="single", label_visibility="hidden",
            default="preview", key="markdown_selection",
        )
            
        if selection == "preview":
            st.markdown(md_cont)
        elif selection == "raw":
            st.code(md_cont, language="markdown")
        elif selection == "images":
            st.subheader("Extracted Images")
            for image_path in image_paths:
                st.image(image_path)
                    
    with html:
        options = ["preview", "raw", "images"]
            
        selection = st.segmented_control(
            "HTML Views", options, selection_mode="single", label_visibility="hidden",
            default="preview", key="html_selection",
        )
            
        if selection == "preview":
            st.write(":(")
        elif selection == "raw":
            st.write(":(")
        elif selection == "images":
            st.subheader("Extracted Images")
            for image_path in image_paths:
                st.image(image_path)