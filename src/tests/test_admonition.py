import pytest

from lib.admonition import admonitions


@pytest.fixture
def admonitions_obsidian() -> str:
    return "> [!tip] Something\n> [!info] More Things\n> [!info] More Things\n> [!warning] Nothing"

@pytest.fixture
def admonitions_devto() -> str:
    return "> **🟢 Tip** - Something\n> **ℹ️ Info** - More Things\n> **ℹ️ Info** - More Things\n> **⚠️ Warning** - Nothing"

def test_format_admonitions_for_dev_to(
    admonitions_obsidian: str, admonitions_devto: str
) -> None:

    expected_result: str = admonitions_devto
    result: str = admonitions_obsidian

    for admonition in admonitions:
        result: str = result.replace(admonition.obsidian, admonition.devto)

    assert expected_result == result

