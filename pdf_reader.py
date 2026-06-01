import io
import fitz  # PyMuPDF


def read_pdf(uploaded_file):
    """
    Read a Streamlit UploadedFile and return (text, page_count).
    Uses BytesIO wrapper for PyMuPDF compatibility.
    """
    # Read all bytes from the Streamlit file object
    raw_bytes = uploaded_file.getvalue()          # getvalue() always works on UploadedFile
    pdf_stream = io.BytesIO(raw_bytes)            # wrap in BytesIO for PyMuPDF

    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    page_count = len(doc)

    text_parts = []
    for page in doc:
        text_parts.append(page.get_text("text"))
    doc.close()

    full_text = "\n".join(text_parts).strip()
    return full_text, page_count
