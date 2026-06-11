import pyclip


def paste_clip() -> str:
    try:
        text = pyclip.paste(text=True)
        if text:
            return str(text)
        else:
            return ""
    except Exception as e:
        print(f"Error {e}")

    return "Nothing is copied..."
