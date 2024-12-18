import os
import pprint
import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from dataclasses import make_dataclass


workflow_path:str = ".github/workflows/verify_getting_started.yml"


def dict_to_object(name: str, dictionary: dict[str, str]):
    fields = [(key, type(value), value) for key, value in dictionary.items()]
    DynamicClass = make_dataclass(name, fields)
    return DynamicClass(**dictionary)


def query_code_from_workflow(file_name:str, job_name:str, step_name:str) -> str:
    with open(file_name, "r") as file:
        yaml_content = yaml.safe_load(file)

    steps: dict[str, str] = yaml_content["jobs"][job_name]["steps"]
    # TODO move conversion out of this function
    name_to_run = {step["name"]: step.get("run") for step in steps}
    return name_to_run[step_name]


input_file = "./ansible_molecule/getting_started/Ansible Molecule using Vagrant & Virtualbox.md"

with open(input_file, "r") as file:
    md_content: str = file.read()

md = MarkdownIt()
tokens: list[Token] = md.parse(md_content)

# for token in tokens:
#     if token.type == "fence" and token.info == "reference":
#         yaml_content = yaml.safe_load(token.content)
#         yaml_obj = dict_to_object(name="yamlObject", dictionary=yaml_content)
#         file_reference: str = yaml_obj.file

#         if file_reference.endswith(os.path.basename(workflow_path)):
#             workflow_code: str = query_code_from_workflow(
#                 file_name=workflow_path,
#                 job_name="molecule-setup-ci",
#                 step_name=yaml_obj.title
#                 )

# query code reference fields
# get referenced file per field
# if file is workflow look for steps with same name
# -> replace code reference with step code
# default: replace with referenced file content
# write new markdown file?

result:str = query_code_from_workflow(
    file_name=workflow_path,
    job_name="molecule-setup-ci",
    step_name="Setup role and molecule scenario"
    )

pprint.pprint(result)
