from src.lib import code_block, admonition, io
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
step_to_code_map:dict[str, str] = code_block.map_step_name_to_code(
        workflow_file=workflow_path,
        job_name="molecule-setup-ci",
    )

md = MarkdownIt()

md_content: str = io.read_file(input_file)
tokens: list[Token] = md.parse(md_content)
code_map_list: list[code_block.CodeMap] = code_block.map_reference_to_source(workflow_path=workflow_path, tokens=tokens, step_to_code_map=step_to_code_map)
export_content: str = code_block.update_text(md_content, code_map_list)
for admonition in admonition.admonitions:
    export_content: str = export_content.replace(admonition.obsidian, admonition.devto)

io.write_file(output_file, export_content)
