# Take

Take manages your local programming projects. It takes care of dependencies and your programming environment.
Take can act as an alias for the Python interpreter, but modifies `PYTHONPATH` so your projects can import eachother.
The same is done for C (not yet). See `take help` for more details.

## Requirements

- `python > 3.10`
- `git`
- the `which` command. Available on most POSIX systems.

## Support
Take is very unstable, and only tested on Fedora Linux 39. Expect bugs and errors.

## Installing

The following section explains the installation. Linux is recommended, but Mac OS will probably work

Take needs a directory where all your projects will be. In that directory you have to clone this repo.
```sh
$ mkdir dev    # This example names the directory 'dev'
$ cd dev
$ git clone https://github.com/vsthijs/take
```
After downloading the repository, you have to install it.
```sh
$ cd take
$ python install.py  # this installs the script to a location that will be on path.
```
To make sure that the `take` command is on path, add the following line to `~/.bashrc`
```bash
export PATH="$PATH:$HOME/dev/take/bin"
```
The path to export is always the `bin` directory in the take repository. When skipping this step,
you will be warned by default.

## Configuring

There are no fancy config files for Take, but can modify the source code to match your preferences.
You should always modify the `take/takecli/main.py` file. After applying the mods, you can execute
`take reload` which repeats some steps described in the installation

Somethings to configure/add:
- colored output
- different C compiler preferences

## Projects

Every `take` project has a configuration file name `take.toml`. I here is information like the author, name and version.
You can also register custom commands that can be executed by `take this <command>` when being in the project.
