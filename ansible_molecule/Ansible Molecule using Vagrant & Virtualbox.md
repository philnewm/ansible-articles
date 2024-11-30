---
tags:
  - ansible
  - molecule
  - automation
  - blog
---
# Getting started with Molecule
## Intro

After reading through a bunch of Ansible molecule setup guides I noticed quite a bunch of them were outdated in at least one critical aspect. Will discuss the details of this in [[#Prepare development environment]]
So this is a guide on setting up Ansible Molecule for testing Ansible roles by running them against virtual machines. These virtual machines will be controlled by vagrant using VirtualBox as provider.
This was tested last on @@TODO insert date and works for the versions mentioned in [[#Requirements]]

## Requirements

First install a bunch of python packages like Ansible, Molecule and its vagrant plugin.
For this to work you will need python >= 3.10 installed.
The docker python package also gets installed here cause `molecule reset` seems to fail when it's not installed.
This step requires **pip** to be installed.

> [!tip] Additionally I recommend creating a [python virtual environment](https://realpython.com/python-virtual-environments-a-primer/) for Ansible first.

On Debian-based systems like Ubuntu you might need to install python-venv first.
`sudo apt-get install python3.10-venv`

Create a python virtual environment and activate it from your terminal like this:
```code
{{CODE:Create environment}}
```

* requires python >=3.10
* install `python3.11` on rhel systems like almalinux9
* install pip by running `python3.11 -m ensurepip`

Create a project directory and `cd` into it.
Create a `requirements.txt` file containing these lines:
```code
{{CODE:Write requirements}}
```

And run you can upgrade pip (just to be sure) and install the requirements
```code
{{CODE:Install requirements}}
```

Additionally Virtualbox and Vagrant are required to follow along.
See the following table for download pages and version used for the following examples.
@@ TODO explain briefly what vagrant is - link to docs

| Tool       | Download Page                                                       | Version used here |
| ---------- | ------------------------------------------------------------------- | ----------------- |
| Virtualbox | [Installers](https://www.virtualbox.org/wiki/Downloads)             | 7.1.4             |
| Vagrant    | [Install commands](https://developer.hashicorp.com/vagrant/install) | 2.4.3             |
 
# Prepare development environment

While I was trying to understand molecule I came across many guides mentioning the command `molecule role init`. 
This one doesn't exist anymore since version [6.0.0](https://github.com/ansible/molecule/releases/tag/v6.0.0) - it was removed intentional to get rid of the [Ansible-Galaxy](https://github.com/ansible/galaxy) dependency.

> [!info]- Code first, explanation second @@TODO move somewhere else
> I for any code examples in this article I'll provide the code frist and explain it afterwards.

```code
{{CODE:Setup role and molecule scenario}}
```

Here we start by creating a new role structure, change into Ansible role directory and initialize a molecule scenario using `molecule init `.
For now I'll just go with the *default* scenario to keep it simple.
Now you got a "molecule" directory inside the role containing a bunch of default .yml files.

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

## How-To-Example

Creating a molecule instance is done by running `molecule create` if you do that right away from the roles root directory you will most likely encounter the following error:
```code
ERROR    Computed fully qualified role name of sample does not follow current galaxy requirements.
Please edit meta/main.yml and assure we can correctly determine full role name:

galaxy_info:
role_name: my_name  # if absent directory name hosting role is used instead
namespace: my_galaxy_namespace  # if absent, author is used instead
```
This happens due to molecule running a [role name-check](https://ansible.readthedocs.io/projects/molecule/configuration/#role-name-check) by default.
As stated in the documentation you can either disable the check or just add the `role_name` and `namespace` to the `meta/main.yml` file.

Now running `molecule create` should, while throwing a bunch of warnings, already work.
Running `moelcule list` should now show this table.
```code
	         ╷           ╷                ╷             ╷       ╷        Instance Name│Driver Name│Provisioner Name│Scenario Name│Created│Converged ─────────────┼───────────┼────────────────┼─────────────┼───────┼───────────╴
  instance   │ default   │ ansible        │ default     │ true  │ false      
             ╵           ╵                ╵             ╵       ╵            
```

This will create a default instance using the [delegated driver](https://ansible.readthedocs.io/projects/molecule/configuration/#delegated), which is just called "default".

As the title suggests we will go for vagrant with Virtualbox as a provider in this example.
So run `molecule destroy` to remove that default instance again.
If you run `molecule drivers` you should see a list of drivers including `vagrant`.

Now edit the molecule config file `molecule/default/molecule.yml` and add vagrant and Virtualbox like this:



When just running `molecule create` from the roles root directory and afterwards running `molecule list`you will get something like this (removed a few blanks to make it fit):


Now we know it works but this default instance isn't too useful so run `molecule destroy` to delete it again.
Next edit the molecule.yml file at `<rolen-name>/molecule/default/molecule.yml`
## Vagrant
Explain what gets saved where and how does the ephemeral directory work

## Virtual Box
* Explain vdisk-type chosen intentionally due to dynamic size allocation

