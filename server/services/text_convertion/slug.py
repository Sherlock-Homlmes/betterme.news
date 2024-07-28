import re
from .language import convert_text_to_standard_type


def gen_slug(s: str) -> str:
    """Generates a slug from the given text, handling various cases."""
    s = convert_text_to_standard_type(s)
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s
