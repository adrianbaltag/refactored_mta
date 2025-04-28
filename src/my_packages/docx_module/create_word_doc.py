import os

from docx import Document


def create_word_doc(filename="New_Document.docx", content=None, title=None):
    """
    Creates a Word document on the desktop

    Args:
        filename (str): Name of the document (include .docx extension)
        content (list): List of paragraphs to add to the document
        title (str): Title to add at the beginning of the document

    Returns:
        str: Path to the created document
    """
    # Create a new Document
    doc = Document()

    # Add title if provided
    if title:
        doc.add_heading(title, level=0)

    # Add content if provided
    if content:
        for paragraph in content:
            doc.add_paragraph(paragraph)

    # Get desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Create full path for the document
    doc_path = os.path.join(desktop_path, filename)

    # Save the document
    doc.save(doc_path)

    return doc_path


# Example usage
if __name__ == "__main__":
    doc_path = create_word_doc()

    print(f"Document created at: {doc_path}")
