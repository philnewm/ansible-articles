from typing import NamedTuple


class Admonition:
    def __init__(self, type: str) -> None:
        self.type: str = type

    @property
    def obsidian(self) -> str:
        return f"> [!{str(self.type)}]"

    @property
    def devto(self) -> str:
        return f"> **{admonition_icons[self.type]} {self.type.capitalize()}** -"

    @property
    def medium(self) -> str:
        return f"> **{admonition_icons[self.type]} {self.type.capitalize()}** -"


class AdmonitionTypesObsidian(NamedTuple):
    abstract: str = "abstract"
    info: str = "info"
    todo: str = "todo"
    tip: str = "tip"
    success: str = "success"
    question: str = "question"
    warning: str = "warning"
    failure: str = "failure"
    danger: str = "danger"
    bug: str = "bug"
    example: str = "example"
    quote: str = "quote"


admonition_icons: dict[str, str] = {
    "abstract": "🗒️",
    "info": "ℹ️",
    "todo": "☑️",
    "tip": "🟢",
    "success": "✔️",
    "question": "❔",
    "warning": "⚠️",
    "failure": "❌",
    "danger": "⚡",
    "bug": "🐛",
    "example": "🧪",
    "quote": "💬",
}


def build_admonitions_list() -> list[Admonition]:
    admonition_list: list[Admonition] = []

    for type in AdmonitionTypesObsidian._fields:
        admonition_list.append(Admonition(type=type))

    return admonition_list
