import re

import pytest


@pytest.fixture()
def get_out_text(capsys):
    def out_text():
        out = capsys.readouterr().out
        out = strip_non_visible(out)
        print(out)
        return out

    return out_text


NON_VISIBLE = [
    "\x1b[0m",
    "\x1b[1m",
    "\x1b[33m",
    "\x1b[36m",
    "\x1b[39m",
    "\x1b[92m",
]


def strip_non_visible(text):
    for nv in NON_VISIBLE:
        text = text.replace(nv, "")
    text = re.sub(r"[ ]+\n", r"\n", text)
    return text
