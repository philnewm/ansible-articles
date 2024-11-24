## Project-Scope

This is a quick overview of the key points I wanted to achieve with this project.

### What?

The project is intended to provide an Ansible development and testing environment that works for gnome-desktop applications on a Linux system.
Therefor it's required to include a GUI for interactive testing during local development. 

### Why?

The resulting Ansible roles are intended to install and configure desktop applications under Gnome for Linux based virtual machines and bare-metal systems.

### How?

To get started I choose vagrant boxes using virtualbox as provider.
To speed things up, I built a bunch of custom vargant boxes that already include a customized gnome desktop. (Note: At the state of writing this the CentOSStream9 Box is broken due to issues with building the virtualbox guest additions during box build)
This allows for interactive testing while still enabling fully automated test runs in terminal.

## Terms [[Terms]]

## Getting Started [[Ansible Molecule using Vagrant & Virtualbox]]
## [[Custom-Setup]]
## [[CI in Github Actions]]

## [[Tags]]
