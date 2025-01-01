from pathlib import Path

import pytest

from src.lib import code_block


@pytest.fixture
def test_workflow() -> dict[str, dict[str, dict[str, list[dict[str, str]]]]]:
    return {
        "jobs": {
            "test_job": {
                "steps": [
                    {"name": "First Task", "run": "echo 'First Task'"},
                    {"name": "Second Task", "run": "echo 'Second Task'"},
                    {"name": "Third Task", "run": "echo 'Third Task'"},
                ]
            },
        }
    }


@pytest.fixture
def code_ref_meta_workflow(tmp_path: Path) -> code_block.CodeReferenceMeta:
    workflow_file: str = "test_workflow.yml"
    code_reference: Path = tmp_path / workflow_file
    return code_block.CodeReferenceMeta(
        file_path=code_reference, title="First Task", language="bash"
    )


def test_map_step_name_to_code(test_workflow: dict[str, dict]) -> None:
    """
    Given a test dictionary resambling a github workflow script.
    When running the map conversion
    Than provide the expected dictionary
    """

    expected_result: dict[str, str] = {
        "First Task": "echo 'First Task'",
        "Second Task": "echo 'Second Task'",
        "Third Task": "echo 'Third Task'",
    }

    result: dict[str, str] = code_block.map_step_name_to_code(
        gh_workflow=test_workflow, job_name="test_job"
    )

    assert isinstance(result, dict)
    assert expected_result == result


def test_parse_workflow_code(
    code_ref_meta_workflow: code_block.CodeReferenceMeta,
    test_workflow: dict[str, dict[str, dict[str, list[dict[str, str]]]]],
) -> None:

    step_to_code_map: dict[str, str] = code_block.map_step_name_to_code(
        gh_workflow=test_workflow,
        job_name="test_job",
    )

    expected_result = "echo 'First Task'"
    result_key: str = code_block.parse_workflow_code(
        reference_meta=code_ref_meta_workflow,
        jobs=step_to_code_map.keys(),
    )
    result: str = step_to_code_map[result_key]

    assert isinstance(result, str)
    assert expected_result == result
