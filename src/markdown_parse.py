import os
import logic

from markdown_it import MarkdownIt
from markdown_it.token import Token
from pathlib import Path

# TODO implement pre commit hook that enforces an empty line at the end of each file


# TODO make it run from src directory right away - doesn't work for worhflow file so far
script_dir = Path(__file__).resolve().parent
root_dir = script_dir.parent

root_dir = script_dir.parent
input_file = root_dir / "ansible_molecule/getting_started/Ansible Molecule using Vagrant & Virtualbox.md"
workflow_path = root_dir / ".github/workflows/run_code_snippets.yml"
output_file = root_dir / "blog/docs/getting_started.md"
md = MarkdownIt()

md_content = logic.read_file(input_file)
tokens: list[Token] = md.parse(md_content)
code_map_list: list[logic.CodeMap] = logic.map_reference_to_source(workflow_path=workflow_path, tokens=tokens)
export_content: str = logic.update_text(md_content, code_map_list)
logic.write_file(output_file, export_content)
