import pdfplumber

def extract_pdf(pdf_path):
    """ Extract the text from the PDF and returns it as a String """
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text   

def save_raw_text(text, output_path):
    """ Writes the extracted text to a .txt file """
    with open(output_path, "w") as f:
        f.write(text)