"""`__init__.py`__
This module initializes the 'docx' package.
"""

from .create_word_doc import create_word_doc
from .update_word_docx import update_word_docx
from .update_word_text import update_word_text

__all__ = ["create_word_doc", "update_word_docx", "update_word_text"]
