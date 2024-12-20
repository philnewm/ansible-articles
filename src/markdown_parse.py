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

input_file = "./ansible_molecule/getting_started/testing.md"

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
# update token values for code snippets
# combine content back together
# overwrite previous file

def map_step_name_to_code(workflow_file: str, job_name: str) -> dict[str, str]:
    
    with open(workflow_file, "r") as file:
        yaml_content = yaml.safe_load(file)

    steps: dict[str, str] = yaml_content["jobs"][job_name]["steps"]

    return {step["name"]: step.get("run") for step in steps}


step_name: str = "Setup role and molecule scenario"


md = MarkdownIt()

with open(input_file, "r") as file:
    md_content: str = file.read()

tokens: list[Token] = md.parse(md_content)

result:dict[str, str] = map_step_name_to_code(
    workflow_file=workflow_path,
    job_name="molecule-setup-ci",
    )

# updated_md_content: str = "".join(token.content if token.content else token.markup + "\n" for token in tokens)

reconstructed_content = ""

for index, token in enumerate(tokens):
    token: Token = tokens[index]
    if token.type == "heading_open":
        heading: str = f"{token.markup} {tokens[index + 1].content} {tokens[index + 2].markup}\n"
        reconstructed_content += heading
        continue

    if token.type == "fence":
        reconstructed_content += f"\n```{token.info}\n{token.content}```\n\n"
        continue

    if token.type == "paragraph_open" and tokens[index-1].type != "list_item_open":
        reconstructed_content += "\n"

    if token.type == "paragraph_close" and tokens[index-1].type != "list_item_close":
        reconstructed_content += "\n"

    if token.type == "bullet_list_open" or token.type == "bullet_list_close":
        reconstructed_content += "\n"

    if token.type == "list_item_open":
        list_item: str = f"{token.markup} {tokens[index + 2].content}"
        continue

    if token.content and tokens[index-1].type != "heading_open":
        reconstructed_content += f"{token.content}"

print(reconstructed_content)