import pprint
import yaml
from typing import NamedTuple
from markdown_it import MarkdownIt
from markdown_it.token import Token
from dataclasses import make_dataclass


workflow_path:str = "./.github/workflows/verify_getting_started.yml"


def dict_to_object(name: str, dictionary: dict[str, str]):
    fields = [(key, type(value), value) for key, value in dictionary.items()]
    DynamicClass = make_dataclass(name, fields)
    return DynamicClass(**dictionary)

def map_step_name_to_code(workflow_file: str, job_name: str) -> dict[str, str]:
    
    with open(workflow_file, "r") as file:
        yaml_content = yaml.safe_load(file)

    steps: dict[str, str] = yaml_content["jobs"][job_name]["steps"]

    return {step["name"]: step.get("run") for step in steps}

def get_code_from(file_path):
    with open(file_path, "r") as file:
        code = file.read()

    return code

step_name: str = "Setup role and molecule scenario"
input_file = "./ansible_molecule/getting_started/Ansible Molecule using Vagrant & Virtualbox.md"

md = MarkdownIt()

with open(input_file, "r") as file:
    md_content = file.read()
tokens: list[Token] = md.parse(md_content)

class code_map(NamedTuple):
    reference: str
    source_code: str


step_to_code_map:dict[str, str] = map_step_name_to_code(
    workflow_file=workflow_path,
    job_name="molecule-setup-ci",
    )

def get_code(code_file: str, workflow_path: str= "", title: str=""):
    if code_file == workflow_path:
        if title not in step_to_code_map.keys():
            raise ValueError(f"Couldn't find step name '{title}' in workflow")

        return step_to_code_map[title]

    return get_code_from(file_path=code_file)

code_map_list: list[code_map] = []

for token in tokens:
    if token.type == "fence" and token.info=="reference":
        reference_dict: dict[str, str] = yaml.safe_load(token.content)
        
        file_path = reference_dict["file"]
        code_title = reference_dict["title"]
        code_laguage = reference_dict["language"]
        
        source_code = get_code(
            code_file=file_path,
            workflow_path=workflow_path,
            title=code_title,
            )
        
        source_code_formatted = f"\n```{code_laguage}\n{source_code}```"
        code_reference = f"{token.markup}{token.info}\n{token.content}{token.markup}"

        code_map_list.append(code_map(reference=code_reference, source_code=source_code_formatted))

export_content = md_content
for code_map in code_map_list:
    export_content = export_content.replace(code_map.reference, code_map.source_code)

output_file = "output.md"
with open(output_file, "w") as file:
    file.write(export_content)
