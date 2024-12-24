import yaml

from markdown_it import MarkdownIt
from markdown_it.token import Token
from typing import NamedTuple


class CodeMap(NamedTuple):
    reference: str
    source_code: str


def read_file(file_path: str):
    """Read a text file

    Args:
        input_file (str): Path to file

    Returns:
        str: file content
    """

    with open(file_path, "r") as file:
        content = file.read()
    
    return content


def write_file(file_path: str, content: str):
    """Write a text file

    Args:
        file_path (str): Path to write to
        content (str): Content to write
    """

    with open(file_path, "w") as file:
        file.write(content)


def map_step_name_to_code(workflow_file: str, job_name: str) -> dict[str, str]:
    """Convert a Github Actions job from yaml format to a dictionary.
    
    Converts a GitHub Actions job steps to a {step-name: run-code} dictionary.

    Args:
        workflow_file (str): Yaml file containing a Github Actions workflow
        job_name (str): Job name to use as source

    Returns:
        dict[str, str]: Step-name as key and Step run-code as value
    """

    with open(workflow_file, "r") as file:
        yaml_content = yaml.safe_load(file)

    steps: dict[str, str] = yaml_content["jobs"][job_name]["steps"]

    return {step["name"]: step.get("run") for step in steps}


def get_code(code_file: str, step_to_code_map: dict[str, str], workflow_path: str, title: str):
    """Get code either from file or workflow.

    Args:
        code_file (str): file path
        workflow_path (str): Relevant workflow path
        title (str): Step name to look for

    Raises:
        ValueError: In case the step name wasn't found in the workflow.

    Returns:
        str: code as text
    """
    
    if code_file == workflow_path:
        if title not in step_to_code_map.keys():
            raise ValueError(f"Couldn't find step name '{title}' in workflow")

        return step_to_code_map[title]

    return read_file(file_path=code_file)


def map_reference_to_source(workflow_path:str, tokens:list[Token]):
    """Map the code references to the source code they point to.

    Args:
        workflow_path (str): Path to GitHub Action workflow
        tokens (list[Tokens]): Token list from parsed markdown file

    Returns:
        list[CodeMap]: List of code mappings
    """

    code_map_list: list[NamedTuple] = []

    step_to_code_map:dict[str, str] = map_step_name_to_code(
        workflow_file=workflow_path,
        job_name="molecule-setup-ci",
    )

    for token in tokens:
        if token.type == "fence" and token.info=="reference":
            reference_dict: dict[str, str] = yaml.safe_load(token.content)
            file_path = reference_dict["file"]
            code_title = reference_dict["title"]
            code_laguage = reference_dict["language"]

            source_code = get_code(
            code_file=file_path,
            step_to_code_map=step_to_code_map,
            workflow_path=workflow_path,
            title=code_title,
            )
            source_code_formatted = f"```{code_laguage}\n{source_code}```"
            code_reference = f"{token.markup}{token.info}\n{token.content}{token.markup}"

            code_map_list.append(CodeMap(reference=code_reference, source_code=source_code_formatted))

    return code_map_list


def update_text(source_text: str, code_map_list:list[CodeMap]):
    """Repalce source text with referenced code.

    Args:
        source_text (str): Code reference
        code_map_list (list[CodeMap]): List of reference to code maps

    Returns:
        str: Updated text output
    """

    export_content = source_text
    for CodeMap in code_map_list:
        export_content = export_content.replace(CodeMap.reference, CodeMap.source_code)

    return export_content
