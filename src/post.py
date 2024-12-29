from lib import connect

def get_markdown_content(markdown_path) -> str:
    with open(markdown_path, "r") as file:
        markdown_content: str = file.read()
    return markdown_content


markdown_content: str = get_markdown_content(
    "ansible_molecule/getting_started/testing.md"
)
post = connect.RestPost(
    api_key="Du61tRudz2KG7BExWJPcr8Un",
    api_endpoint="https://dev.to/api/articles",
    title="Test Title",
    payload=markdown_content,
    status=False,
    tags=["python", "ansible", "automation", "testing"],
    canonical_url="https://philnewm.github.io/ansible-articles/getting_started/"
    )
post.upload()
