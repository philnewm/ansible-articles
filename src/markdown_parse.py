import logic

from markdown_it import MarkdownIt
from markdown_it.token import Token


input_file: str = "./ansible_molecule/getting_started/Ansible Molecule using Vagrant & Virtualbox.md"
workflow_path: str = "./.github/workflows/verify_getting_started.yml"
md = MarkdownIt()
output_file = "output.md"

md_content = logic.read_file(input_file)
tokens: list[Token] = md.parse(md_content)
code_map_list = logic.map_reference_to_source(workflow_path=workflow_path, tokens=tokens)
export_content = logic.update_text(md_content, code_map_list)
logic.write_file(output_file, export_content)
