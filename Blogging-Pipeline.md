# Automate Blogging
## Requirements
* Full data control - independent of blogging services
* Preferably only local text files
* Upload to multiple sites
* Automatically test code examples

## Tools
* Obsidian
* Github
* Github Actions
* Github Pages
* Dev.to API
* Medium API

## Pipeline-Approach
* Write markdown files locally in obsidian
* Include code previews from external files or even web resources like GitHub
* Replace code previews on push by GitHub action
* Research markdown support and features per blogging host site
* RnD if obsidian callout like feature exists on other services too
* Streamline Blog structure

## Github Actions

* Reset directory for each step
* Set python [virtual environment globally](https://adamj.eu/tech/2023/11/02/github-actions-faster-python-virtual-environments/) for a job
* Set working directory + shell per step [source](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/setting-a-default-shell-and-working-directory)
```yaml
defaults:
  run:
    shell: bash
    working-directory: ./scripts
```
