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

input_file = "./ansible_molecule/getting_started/Ansible Molecule using Vagrant & Virtualbox.md"

def map_step_name_to_code(workflow_file: str, job_name: str) -> dict[str, str]:
    
    with open(workflow_file, "r") as file:
        yaml_content = yaml.safe_load(file)

    steps: dict[str, str] = yaml_content["jobs"][job_name]["steps"]

    return {step["name"]: step.get("run") for step in steps}


step_name: str = "Setup role and molecule scenario"


md = MarkdownIt()

in_ref_code_block = False
code_block_yaml: str = ""
updated_lines: list[str] = []

with open(input_file, "r") as file:
    # md_content: str = file.read()
    for line in file:
        if line.startswith("```reference"):
            in_ref_code_block = True
            continue

        if in_ref_code_block:
            code_block_yaml += line

        if line.startswith("```") and in_ref_code_block:
            in_ref_code_block = False
            updated_lines.append(f"```yaml\n{code_block_yaml}```")
            code_block_yaml = ""
            continue



# tokens: list[Token] = md.parse(md_content)

result:dict[str, str] = map_step_name_to_code(
    workflow_file=workflow_path,
    job_name="molecule-setup-ci",
    )

# updated_md_content: str = "".join(token.content if token.content else token.markup + "\n" for token in tokens)

# reconstructed_content: str = ""

# for index, token in enumerate(tokens):
#     if token.type == "heading_close":
#         if token.tag != "h1":
#             reconstructed_content += "\n"
 
#         heading: str = f"{tokens[index - 2].markup} {tokens[index - 1].content}\n\n"
#         reconstructed_content += heading
#         continue

#     if token.type == "fence":
#         reconstructed_content += f"\n```{token.info}\n{token.content}```\n\n"
#         continue

#     if token.type == "paragraph_close":
#         reconstructed_content += "\n"
#         continue

#     if token.type == "list_item_open":
#         reconstructed_content += f"{token.markup} {tokens[index+2].content}"
#         continue

#     if token.type == "bullet_list_open":
#         reconstructed_content += "\n"
#         continue

#     if token.type == "bullet_list_close":
#         reconstructed_content += "\n"
#         continue

#     if token.content:
#         if tokens[index-1].type == "heading_open":
#             continue

#         if tokens[index-2].type == "list_item_open":
#             continue

#         reconstructed_content += f"{token.content}"

# print(reconstructed_content)

# output_file = "output.md"
# with open(output_file, "w") as file:
#     file.write(reconstructed_content)