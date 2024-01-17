# Take

Take manages your local projects. It takes care of dependency and your programming environment.
Take can act as an alias for the Python interpreter, but modifies `PYTHONPATH` so your projects can import eachother. The same is done for C (not yet). See `take help` for more details.

## Requirements

- `python > 3.10`
- `git`
- the `which` command. Available on most POSIX systems.

## Installing

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
The path to export is always the `bin` directory in the take repository.

## Configuring

There are no fancy config files for Take, but can modify the source code to match your preferences.
You should always modify the `take/takecli/main.py` file. After applying the mods, you can execute
`take reload` which repeats some steps described in the installation

Somethings to configure/add:
- colored output
- different C compiler preferences
