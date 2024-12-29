from lib import code_format, admonitions_format

from markdown_it import MarkdownIt
from markdown_it.token import Token
from pathlib import Path

# TODO implement pre commit hook that enforces an empty line at the end of each file


# TODO make it run from src directory right away - doesn't work for worhflow file so far
script_dir: Path = Path(__file__).resolve().parent
root_dir: Path = script_dir.parent

root_dir = script_dir.parent
input_file: Path = root_dir / "ansible_molecule/getting_started/Ansible Molecule using Vagrant & Virtualbox.md"
workflow_path: Path = root_dir / ".github/workflows/run_code_snippets.yml"
output_file: Path = root_dir / "blog/docs/devto_test.md"
md = MarkdownIt()

md_content: str = code_format.read_file(input_file)
tokens: list[Token] = md.parse(md_content)
code_map_list: list[code_format.CodeMap] = code_format.map_reference_to_source(workflow_path=workflow_path, tokens=tokens)
export_content: str = code_format.update_text(md_content, code_map_list)
for admonition in admonitions_format.build_admonitions_list():
    export_content: str = export_content.replace(admonition.obsidian, admonition.devto)

code_format.write_file(output_file, export_content)
