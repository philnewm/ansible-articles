import pytest

from src.lib import code_block


@pytest.fixture
def test_workflow() -> dict[str, dict[str, dict[str, list[dict[str, str]]]]]:
    return {
        "jobs": {
            "test_job": {
                "steps": [
                    {
                        "name": "First Task",
                        "run": "echo 'First Task'"
                    },
                    {
                        "name": "Second Task",
                        "run": "echo 'Second Task'"
                    },
                    {
                        "name": "Third Task",
                        "run": "echo 'Third Task'"
                    }
                ]
            },
        }
    }


def test_map_step_name_to_code(test_workflow: dict[str, dict]) -> None:
    """
    Given a test dictionary resambling a github workflow script.
    When running the map conversion
    Than provide the expected dictionary
    """

    expected_result: dict[str, str] = {
        "First Task": "echo 'First Task'",
        "Second Task": "echo 'Second Task'",
        "Third Task": "echo 'Third Task'"
    }

    result: dict[str, str] = code_block.map_step_name_to_code(gh_workflow=test_workflow, job_name="test_job")

    assert isinstance(result, dict)
    assert expected_result == result
