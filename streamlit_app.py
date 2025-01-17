from streamlit_javascript import st_javascript
from parser import Parser
import streamlit as st
import markdown
import tempfile

st.set_page_config(
    page_title="UN-PDF",
    page_icon= '<?xml version="1.0" encoding="UTF-8"?><svg id="Layer_2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60.6 37.5"><defs><style>.cls-1{fill:#231f20;}</style></defs><g id="Layer_1-2"><path class="cls-1" d="M18.75,37.5C5.22,37.5,0,30.8,0,20.24V1.43C0,.49.44,0,1.43,0h20.57c.93,0,1.43.49,1.43,1.43v18.81c0,6.71,2.75,10.78,8.96,10.78h9.46c6.27,0,9.18-4.07,9.18-10.78V1.43c0-.94.5-1.43,1.49-1.43h6.6c.99,0,1.48.49,1.48,1.43v18.81c0,9.62-5.94,17.27-18.75,17.27h-23.1Z"/></g></svg>',
    layout="centered",
)

# Update default Streamlit styling
hide_decoration_bar_style = '''<style>#stDecoration {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")
if st_theme == "dark":
    banner_path = "images/unpdf_banner.png"
else:
    banner_path = "images/banner_light.png"

st.image(banner_path)
st.subheader("") # Spacing between banner and file upload

input_file = st.file_uploader("Your PDF:", type="pdf")

if input_file:
    # Temporarily save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(input_file.read())
        temp_pdf_path = temp_file.name

    parser = Parser(temp_pdf_path)

    md_cont = parser.parse_markdown()
    md_raw = md_cont.encode()
    html_cont = parser.parse_html()

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
                if not image_paths:
                    st.subheader("No images found")
                else:
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
                st.html(html_cont)
            elif selection == "raw":
                st.code(html_cont, language="cshtml") # no react syntax highlighting for 'html'
            elif selection == "images":
                if not image_paths:
                    st.subheader("No images found")
                else:
                    st.subheader("Extracted Images")
                    for image_path in image_paths:
                        st.image(image_path)