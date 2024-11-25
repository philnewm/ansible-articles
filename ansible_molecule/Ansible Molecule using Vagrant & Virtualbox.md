---
tags:
  - ansible
  - molecule
  - automation
  - blog
---
# Getting started with Molecule
## Intro

After reading through a bunch of Ansible molecule setup guides myself I noticed quite a bunch of them were outdated in at least one critical aspect. Will discuss the details of this in [[#Prepare development environment]]
So this is a guide on setting up Ansible Molecule for testing Ansible roles by running them against virtual machines. These virtual machines will be controlled by vagrant using VirtualBox as provider.
This was tested last on @@TODO insert date and works for the versions mentioned in [[#Requirements]]

## Requirements

First install a bunch of python packages like Ansible, Molecule and its vagrant plugin.
For this to work you will need python installed.
The docker python package also gets installed here cause `molecule reset` seems to fail when it's not installed.
This step requires **pip** to be installed.

> [!tip] Additionally I recommend creating a [python virtual environment](https://realpython.com/python-virtual-environments-a-primer/) for Ansible first.

Might need to install venv first
`sudo apt-get install python3.10-venv`

Create a python virtual environment and activate it from your terminal like this:
```bash
python3 -m venv ~/.venv/ansible_env
source ~/.venv/ansible_env/bin/activate
```

* requires python >=3.10
* install `python3.11` on rhel systems like almalinux9
* install pip by running `python3.11 -m ensurepip`

Create a project directory and `cd` into it.
Create a `requirements.txt` file containing these lines:
```code
ansible==10.6.0
molecule==24.9.0
molecule-plugins[vagrant]
docker==7.1.0
```

And run `python -m pip install -r requirements.txt` to install all of them.

Additionally Virtualbox and Vagrant are required to follow along.
See the following table for download pages and version used for the following examples.

| Tool       | Download Page                                                       | Version used here |
| ---------- | ------------------------------------------------------------------- | ----------------- |
| Virtualbox | [Installers](https://www.virtualbox.org/wiki/Downloads)             | 7.1.4             |
| Vagrant    | [Install commands](https://developer.hashicorp.com/vagrant/install) | 2.4.3             |
 
# Prepare development environment

While I was trying to understand molecule I came across many guides mentioning the command `molecule role init`. 
This one doesn't exist anymore since version [6.0.0](https://github.com/ansible/molecule/releases/tag/v6.0.0) - it was removed intentional to get rid of the [Ansible-Galaxy](https://github.com/ansible/galaxy) dependency.

> [!info]- Code first, explanation second
> I for any code examples in this article I'll provide the code frist and explain it afterwards.

```bash
ansible-galaxy role init <role_name>
cd <role_name>
molecule init scenario <scenario name>
```

Here we start by creating a new role structure by running `ansible-galaxy role init <role_name>` , change into Ansible role directory and initialize a molecule scenario using `molecule init scenario <scenario name>`.
For now I'll just go with the *default* scenario to keep it simple.
This will create a molecule directory inside the role directory containing a bunch of default .yml files.

```code
📦sample_role  
 ┣ 📂defaults  
 ┃ ┗ 📜main.yml  
 ┣ 📂files  
 ┣ 📂handlers  
 ┃ ┗ 📜main.yml  
 ┣ 📂meta  
 ┃ ┗ 📜main.yml  
 ┣ 📂molecule  
 ┃ ┗ 📂default  
 ┃ ┃ ┣ 📜converge.yml  
 ┃ ┃ ┣ 📜create.yml  
 ┃ ┃ ┣ 📜destroy.yml  
 ┃ ┃ ┗ 📜molecule.yml  
 ┣ 📂tasks  
 ┃ ┗ 📜main.yml  
 ┣ 📂templates  
 ┣ 📂tests  
 ┃ ┣ 📜inventory  
 ┃ ┗ 📜test.yml  
 ┣ 📂vars  
 ┃ ┗ 📜main.yml  
 ┗ 📜README.md
```

For details about how each file and directory inside this role structure is supposed to be used see the [Ansible documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-directory-structure)
Just to provide you a quick overview:

| Directory | Puprose                                                           |
| --------- | ----------------------------------------------------------------- |
| defaults  | Any kind of variables which are supposed to be adjusted           |
| files     | Files to copy over to the remote host                             |
| handlers  | Handlers to run at the end of a play                              |
| meta      | Meta for [ansible galaxy](https://galaxy.ansible.com)             |
| molecule  | Molecule testing setup                                            |
| tasks     | The Logic to run this role                                        |
| templates | Usually jinja2 template scripts to template to the remote host    |
| tests     | Files containing tests - can be used in combination with molecule |
| vars      | Variables required for the role - like names of dependencies      |
## How-To-Example

First we need to setup a platform molecule should use.
As the title suggests we will go for vagrant with Virtualbox as a provider in this example.
First we need to add a role name to the meta file otherwise molecule will fail to create an instance. This happens due to a linting process running first.
```code
INFO     default scenario test matrix: dependency, create, prepare
INFO     Performing prerun with role_name_check=0...
ERROR    Computed fully qualified role name of sample does not follow current galaxy requirements.
Please edit meta/main.yml and assure we can correctly determine full role name:

galaxy_info:
role_name: my_name  # if absent directory name hosting role is used instead
namespace: my_galaxy_namespace  # if absent, author is used instead
```

* default warning `WARNING  Skipping, prepare playbook not configured.` - explain non-configured 
* List of drivers `molecule drivers`
* List instances `molecule list`
* default driver is [delegated](https://ansible.readthedocs.io/projects/molecule/configuration/#driver)
* 

When just running `molecule create` from the roles root directory and afterwards running `molecule list`you will get something like this (removed a few blanks to make it fit):
```code
	         ╷           ╷                ╷             ╷       ╷        Instance Name│Driver Name│Provisioner Name│Scenario Name│Created│Converged ─────────────┼───────────┼────────────────┼─────────────┼───────┼───────────╴
  instance   │ default   │ ansible        │ default     │ true  │ false      
             ╵           ╵                ╵             ╵       ╵            
```

Now we know it works but this default instance isn't too useful so run `molecule destroy` to delete it again.
Next edit the molecule.yml file at `<rolen-name>/molecule/default/molecule.yml`
## Vagrant
Explain what gets saved where and how does the ephemeral directory work

## Virtual Box
* Explain vdisk-type chosen intentionally due to dynamic size allocation

