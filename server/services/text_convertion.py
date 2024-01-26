name_check = {
    "ă": "a",
    "â": "a",
    "á": "a",
    "à": "a",
    "ã": "a",
    "ả": "a",
    "ạ": "a",
    "ắ": "a",
    "ằ": "a",
    "ặ": "a",
    "ẵ": "a",
    "ẳ": "a",
    "ầ": "a",
    "ấ": "a",
    "ẩ": "a",
    "ẫ": "a",
    "ậ": "a",
    "đ": "d",
    "ê": "e",
    "è": "e",
    "ẻ": "e",
    "é": "e",
    "ẽ": "e",
    "ẹ": "e",
    "ề": "e",
    "ế": "e",
    "ể": "e",
    "ễ": "e",
    "ệ": "e",
    "ô": "o",
    "ơ": "o",
    "ồ": "o",
    "ố": "o",
    "ổ": "o",
    "ỗ": "o",
    "ộ": "o",
    "ờ": "o",
    "ớ": "o",
    "ở": "o",
    "ỡ": "o",
    "ợ": "o",
    "ò": "o",
    "ó": "o",
    "õ": "o",
    "ỏ": "o",
    "ọ": "o",
    "ư": "u",
    "ừ": "u",
    "ứ": "u",
    "ử": "u",
    "ữ": "u",
    "ự": "u",
    "ù": "u",
    "ú": "u",
    "ũ": "u",
    "ụ": "u",
    "ủ": "u",
    "í": "i",
    "ì": "i",
    "ĩ": "i",
    "ỉ": "i",
    "ị": "i",
    "ỳ": "y",
    "ý": "y",
    "ỵ": "y",
    "ỷ": "y",
    "ỹ": "y",
}

replace_string = {
    ".": "",
    '"': "",
    "'": "",
    "`": "",
    "’": "",
    "‘": "",
    " ": "-",
}


def gen_slug_from_title(name: str) -> str:
    global name_check, replace_string

    name = name.lower()
    for key, value in replace_string.items():
        name = name.replace(key, value)
    while "--" in name:
        name = name.replace("--", "-")
    convert_name = [name_check[x] if x in name_check.keys() else x for x in name]
    return "".join(convert_name)
