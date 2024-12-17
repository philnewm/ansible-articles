import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from types import SimpleNamespace


def dict_to_dot_notation(data):
    """
    Recursively converts a dictionary into an object supporting dot notation.
    Args:
        data (dict): A dictionary to convert.
    Returns:
        SimpleNamespace: An object where keys are accessible as attributes.
    """
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_dot_notation(v) for k, v in data.items()})
    if isinstance(data, list):
        return [dict_to_dot_notation(item) for item in data]

    return data


input_file = "./ansible_molecule/getting_started/Ansible Molecule using Vagrant & Virtualbox.md"

# Read input Markdown file
with open(input_file, "r") as file:
    md_content: str = file.read()

# Initialize Markdown parser
md = MarkdownIt()
tokens: list[Token] = md.parse(md_content)

for token in tokens:
    if token.type == "fence" and token.info == "reference":
        yaml_content = yaml.safe_load(token.content)
        yaml_obj = type('Obj', (object,), {k: v for k, v in yaml_content.items()})()
        print(yaml_obj.file)