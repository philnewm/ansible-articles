# Automate Blogging
## Requirements
* Full data control - independent of blogging services
* Preferably only local text files
* Upload to multiple sites
* Automatically test code examples
* Insert referenced code automatically
* convert obsidian specific syntax like callouts
* Automated check for @@ToDo
* Automated language check
* Automated markdown formatting

## Tools
* Obsidian
* Github
* MkDocs/Hugo/Jekyll
* Github Actions
* Github Pages
* Dev.to API
* Medium API
* [foam](https://foambubble.github.io/foam/)
* [second-brain-automation](https://medium.com/design-bootcamp/automating-my-second-brain-how-technology-makes-information-management-effortless-afb2a1e4ab11)
* [obsidian export](https://github.com/zoni/obsidian-export)

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

## website-conversion
Multiple options available

* Jekyll - works out of the box with github actions and pages due to integration
* MKDocs - easy setup using pip, needs manual build, can be adjusted using python
* Hugo - [Network chuck guide](https://www.youtube.com/watch?v=dnE7c0ELEH8)

## Hugo limitations
* Doesn't support obsidian style callouts out of the box
* Code blocks only et a copy button and that's it
* [Pandoc lua filter](https://github.com/mokeyish/obsidian-enhancing-export/issues/60) might provide a solution

ToDo:
* Get callout interpretation working
* Enhance code blocks to display language, title + collapsible

## Formatting ToDos
* Enable code tabs for multiple code versions in on place in obsidian
* Enable callout conversion through mkdocs