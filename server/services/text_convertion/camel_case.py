from .language import convert_text_to_standard_type


def gen_camel_case(s: str) -> str:
    s = convert_text_to_standard_type(s)
    return "".join(word.capitalize() for word in s.split())
