import re


def capitalize_sentences(text: str) -> str:
    """Return text capitalizing the sentences. Note that sentences can end
       in dot (.), question mark (?) and exclamation mark (!)"""
    ret = ''
    for sentence in re.finditer(r'(.+?[.?!]\s*)', text, flags=re.DOTALL):
        ret += sentence[0][0].upper() + sentence[0][1:]
    return ret
