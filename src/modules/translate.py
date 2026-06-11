import argostranslate.translate


def tranlate_text(text: str) -> str:
    return argostranslate.translate.translate(
        text,
        "en",
        "es",
    )
