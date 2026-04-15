"""PDF parsing module for extracting text from resume PDFs."""
import pdfplumber


def parse_pdf_file(file_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as a single string
        
    Raises:
        IOError: If file cannot be read
        ValueError: If PDF is empty or unreadable
    """
    try:
        text_content = []
        with pdfplumber.open(file_path) as pdf:
            if len(pdf.pages) == 0:
                raise ValueError("PDF file is empty (no pages found)")
            
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        full_text = "\n".join(text_content)
        
        if not full_text or not full_text.strip():
            raise ValueError("No readable text extracted from PDF")
        
        return full_text
    except FileNotFoundError:
        raise IOError(f"PDF file not found: {file_path}")
    except Exception as e:
        if "PDF" in str(type(e).__name__):
            raise ValueError(f"Failed to parse PDF: {str(e)}")
        raise
