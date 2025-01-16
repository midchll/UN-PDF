"""
Note for future
Streamlit st.html() format: "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>" 
"""

import pymupdf4llm
import fitz
import os

class Parser():
    def __init__(self, pdf):
        self.pdf = pdf
        
    def parse_markdown(self):
        return pymupdf4llm.to_markdown(self.pdf)
    
    def extract_images(self, output_folder):
        doc = fitz.open(self.pdf)
        image_paths = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images(full=True)
                                     
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                os.makedirs(output_folder, exist_ok=True)
                
                image_filename = f"page{page_num+1}_img{img_index+1}.{image_ext}"
                image_path = f"{output_folder}/{image_filename}"
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                    
                image_paths.append(image_path)
                
        return image_paths