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
* Virtualization enabled - due to running virtual machines from molecule

> [!tip] Additionally I recommend creating a [python virtual environment](https://realpython.com/python-virtual-environments-a-primer/) for Ansible first.

On Debian-based systems like Ubuntu you might need to install python-venv first.
```reference
title: "Install virtual environment package"
file: ./.github/workflows/verify_getting_started.yml
start: 29
end: "+0"
language: shell
fold: true
ln: true
```

Create a python virtual environment and activate it from your terminal like this:
Create a `requirements.txt` file containing these lines:
```reference
title: "Create virtual environment"
file: ./.github/workflows/verify_getting_started.yml
start: 33
end: "+0"
language: shell
fold: true
ln: true
```

* requires python >=3.10
* install `python3.11` on rhel systems like almalinux9
* install pip by running `python3.11 -m ensurepip`

Create a project directory and `cd` into it.
Create a `requirements.txt` file containing these lines:
```reference
title: "requirements.txt"
file: ./ansible_molecule/getting_started/requirements.txt
language: shell
fold: true
ln: true
```

> [!tip]- docker python packages
> Installing the docker python package is only necessary due to a bug [#32540](https://github.com/ansible/molecule/issues/2540) in molecule plugins.
> A fix for this one is already merged, see [#166](https://github.com/ansible-community/molecule-plugins/issues/166) but no new release happened so far. 

And run you can upgrade pip (just to be sure) and install the requirements
```reference
title: "Install commands on debian-based systems"
file: ./.github/workflows/verify_getting_started.yml
start: 47
end: "+1"
language: shell
fold: true
ln: true
```

Additionally Virtualbox and Vagrant are required to follow along.
See the following table for download pages and version used for the following examples.
@@ TODO explain briefly what vagrant is - link to docs

| Tool       | Download Page                                                       | Version used here |
| ---------- | ------------------------------------------------------------------- | ----------------- |
| Virtualbox | [Installers](https://www.virtualbox.org/wiki/Downloads)             | 7.1.4             |
| Vagrant    | [Install commands](https://developer.hashicorp.com/vagrant/install) | 2.4.3             |

```reference
title: "Install commands on debian-based systems"
file: ./.github/workflows/verify_getting_started.yml
start: 53
end: "+3"
language: shell
fold: true
ln: true
```

```lang:bash fold:true ln:true title:"Install commands on redhat-based systems"
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | rpm --import oracle_vbox_2016.asc
sudo dnf update
sudo dnf install virtualbox-7.1 -y
```
## Prepare development environment

While I was trying to understand molecule I came across many guides mentioning the command `molecule role init`. 
This one doesn't exist anymore since version [6.0.0](https://github.com/ansible/molecule/releases/tag/v6.0.0) - it was removed intentional to get rid of the [Ansible-Galaxy](https://github.com/ansible/galaxy) dependency.

> [!info]- Code first, explanation second @@TODO move somewhere else
> I for any code examples in this article I'll provide the code frist and explain it afterwards.

```reference
title: "Setup role and molecule scenario"
file: ./.github/workflows/verify_getting_started.yml
start: 73
end: "+2"
language: shell
fold: true
ln: true
```

Here we start by creating a new role structure, change into Ansible role directory and initialize a molecule scenario using `molecule init scenario`.
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
 ┃   ┣ 📜converge.yml  
 ┃   ┣ 📜create.yml  
 ┃   ┣ 📜destroy.yml  
 ┃   ┗ 📜molecule.yml  
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

### Default Instance

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
Running `molecule list` should now show this table.
```code
	         ╷           ╷                ╷             ╷       ╷        Instance Name│Driver Name│Provisioner Name│Scenario Name│Created│Converged ─────────────┼───────────┼────────────────┼─────────────┼───────┼───────────
  instance   │ default   │ ansible        │ default     │ true  │ false     
             ╵           ╵                ╵             ╵       ╵           
```

This will create a default instance using the [delegated driver](https://ansible.readthedocs.io/projects/molecule/configuration/#delegated), which is just called "default".
As the title suggests we will go for Vagrant with VirtualBox as a provider in this example.
So run `molecule destroy` to remove that default instance again.
Then try running `molecule reset` to reset or delete the scenario cache at `~/.cache/molecule/<role-name>/<scenario-name>`. This might result in a python-traceback related to docker on RHEL-systems but will still work and remove the directory as expected. 

> [!warning]- Python traceback explanation
> Indicates docker and or the python module isn't installed on your system, see [#166](https://github.com/ansible-community/molecule-plugins/issues/166)
> Happen e.g. on Almalinux 9 due to podman being the default container service instead of docker and molecule doesn't seem to like this.

If you run `molecule drivers` you should see a list of installed drivers including `vagrant`.
Take a look at the [molecule-plugins repository](https://github.com/ansible-community/molecule-plugins/blob/main/README.md) for additional information

### Vagrant Instance

```reference
title: "molecule.yml"
file: ./ansible_molecule/getting_started/molecule.yml
language: yaml
fold: true
ln: true
```
---
> [!info]-
> Assigning a network-interface using a `192.168.56.X` address is crucial here.
> VirtualBox sets up two virtual networks  by default.
> * vboxnet0 - which is Host-only using 192.168.56.1
> * NatNetwork - using 10.0.2.X
> 
> NatNetwork will be used by default but requires port forwarding from the host to the VM to make it accessible from e.g. a browser on the host
> To get around this we just assign a static address from the host-only network.
> 

```reference
title: "Initialize vagrant scenario"
file: ./.github/workflows/verify_getting_started.yml
start: 138
end: "+6"
language: shell
fold: true
ln: true
```
---
Line 1: Initialize a new scenario using explicit parameters to use vagrant
Line 2: The default `create.yml` file will cause connection issues on start-up so we fix this by copying the one from the molecule vagrant plugin itself
Line 3: The default `destroy.yml`file won't destroy the vagrant box itself so we replace it by copying the one from the molecule vagrant plugin itself
Line 4: Now replace the molecule config file `molecule/default/molecule.yml` with the provided one which uses AlmaLinux9.
Other vagrant box options can be found on [vagrant cloud](https://portal.cloud.hashicorp.com/vagrant/discover/almalinux/9)
Line 5: Create the new molecule instance
Line 6: The list should now display the vagrant instance we just configured

### Access Vagrant Instance

Accessing an instance is supposed to be done by running `molecule login`, this is currently not working due to a bug, see this [issue](https://github.com/ansible-community/molecule-plugins/issues/239) and should be resolved with the next release.
In the meantime you can run `vagrant global-status` to get the vagrant instance IDs and `vagrant ssh <id>` to log into one of the VMs displayed. Afterwards just type `exit` to drop out of the instance again.

### Provision a service

After setting up this vagrant instance successfully it is now time to make it do something using Ansible as its provisioner.

```reference
title: "tasks.yml"
file: ./ansible_molecule/getting_started/tasks.yml
language: yaml
fold: true
ln: true
```
---
These 4 Tasks will execute the following actions in order:
1. Gather facts about the VirtualBox VM
2. Install an Apache web-server from the AlmaLinux9 default repositories
3. Start and enable the web-servers service
4. Display the VMs IP address for debugging purposes

Now run `molecule converge` to run these tasks against the VirtualBox VM.
After this ran successfully you should be able to just copy the IP address displayed by the debug task e.g. `192.168.56.10` to your browser and see the default Apache Webserver page right away.

Even tho this is nice, testing the functionality of this web-server manually isn't quite a scaleable approach. So let's also automate this part.


@@TODO might need manual instance deletion otherwise stuck on docker traceback

Now we know it works but this default instance isn't too useful so run `molecule destroy` to delete it again.
Next edit the molecule.yml file at `<rolen-name>/molecule/default/molecule.yml`
## Vagrant
Explain what gets saved where and how does the ephemeral directory work

## Virtual Box
* Explain vdisk-type chosen intentionally due to dynamic size allocation

