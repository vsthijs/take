#!/usr/bin/env python3

import os
import sys
from typing import Any
import tomli, tomli_w
import subprocess


def panic(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    return exit(code)


def home() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # ./../../


def join(*paths: str, base=None) -> str:
    if not base:
        base = home()
    return os.path.join(base, *paths)


def get_list() -> list[str]:
    l = []
    for ii in os.listdir(home()):
        if os.path.isdir(join(ii)):
            l.append(ii)
    return l


def has_package(name: str) -> bool:
    return name in get_list()


def get_package_conf(name: str) -> dict[str, Any] | None:
    if not has_package(name):
        return None
    packpath = join(name)
    if "take.toml" not in os.listdir(packpath):
        return None
    with open(join("take.toml", base=packpath)) as f:
        conf = tomli.loads(f.read())
    return conf


def verify_package_conf(conf: dict[str, Any]) -> str | None:
    if "package" not in conf:
        return "package configuration requires a 'package' section."
    for ii in ["name", "author", "version"]:
        if ii not in conf["package"]:
            return "package configuration requires 'package.{ii}'"


def new_package(name: str, **flags):
    if has_package(name):
        panic(f"package {name} already exists")
    elif " " in name:
        panic(f"package name cannot contain spaces")

    packpath = join(name)
    os.mkdir(join(packpath))
    with open(join("take.toml", base=packpath), "w") as f:
        f.write(
            tomli_w.dumps(
                {
                    "package": {
                        "name": name,
                        "version": "0.0.0",
                    },
                    "dependencies": {},
                }
            )
        )
    with open(join(".gitignore", base=packpath), "w") as f:
        f.write("\n")
    with open(join("readme.md", base=packpath), "w") as f:
        f.write(f"# {name}\n")
    subprocess.call(["git", "init", packpath])


def package_get_cmd(name: str, cmd: str) -> str | None:
    if conf := get_package_conf(name):
        if cmds := conf.get("cmd"):
            if c := cmds.get(cmd):
                return c.get("command")
    return None


def package_get_cmd_list(name: str) -> list[str]:
    if conf := get_package_conf(name):
        if cmds := conf.get("cmd"):
            l = []
            for k in cmds.keys():
                l.append(k)
            return l
        return []
    else:
        panic("no package conf found")


def curr_package() -> str | None:
    if "take.toml" in os.listdir():
        with open("take.toml") as f:
            n = tomli.loads(f.read()).get("package", {}).get("name", None)
        return n if n else None


def shift(arr: list[str]) -> tuple[str, list[str]]:
    return arr[0], arr[1:]


def usage(prog: str) -> str:
    return f"""Usage: {prog} <command> [flags]

See `{prog} help` for more information."""


def usage_long(prog: str) -> str:
    return f"""Usage: {prog} [command] [flags]

Commands:
    help []             Show more documentation.
    new <name> [flags]  Create a new package.
    this <cmd> [flags]  Execute a command, defined by the package.
    clone <name> <url>  Downloads a remote repository using git.
    
    cc [cflags]         Act as a C compiler. Chooses between gcc,clang,cc,
                        zig cc,tcc. Automatically adds -L flags for all
                        projects.
    py script [flags]   Act as a Python interpreter. Automatically includes all
                        take projects in PYTHONPATH so you can import them."""


def cmd_help(args: list[str], prog: str) -> int:
    print(usage_long(prog))
    return 0


def cmd_new(args: list[str], prog: str) -> int:
    if len(args) < 1:
        panic(f"{prog}: new: required argument not given: 'name'")
    name, args = shift(args)
    new_package(name)
    print(f"{prog}: new: package created")
    return 0


def cmd_dbg(args: list[str], prog: str) -> int:
    print(f"program: {prog} -> {__file__}")
    print(f"home: {home()}")
    print(f"packages:")
    for ii in get_list():
        print(f"- {ii} at {join(ii)}")
    return 0


def cmd_this(args: list[str], prog: str) -> int:
    pack = curr_package()
    if not pack:
        panic(
            f"{prog}: this: should be executed inside the directory with the take.toml file."
        )
    defined_commands = package_get_cmd_list(pack)

    if len(args) < 1:
        print("defined commands:")
        for ii in defined_commands:
            print(f"- {ii}")
        panic(f"\n{prog}: this: required argument not given: 'cmd'")
    cmd, args = shift(args)

    if command := package_get_cmd(pack, cmd):
        command = command.replace("@python", "take py")
        command = command.replace("@cc", "take cc")
        old = os.getcwd()
        os.chdir(join(pack))
        print(command)
        res = subprocess.call(command.split(" "))
        os.chdir(old)
        return res
    else:
        panic(f"{prog}: this: {cmd} is not a defined command.")


def cmd_cc(args: list[str], prog: str) -> int:
    for ii in [
        "gcc",
        "clang",
        "cc",
        "zig cc",
        "tcc",
    ]:
        if (
            subprocess.call(
                ["which", ii.split(" ")[0]],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
            == 0
        ):
            return subprocess.call([*ii.split(" "), *args])
    panic(f"{prog}: cc: no c compiler installed on the system.")


def cmd_py(args: list[str], prog: str) -> int:
    env = env = {
        "PYTHONPATH": ":".join(
            [os.environ.get("PYTHONPATH", ""), *[join(ii) for ii in get_list()]]
        )
    }
    subprocess.call([sys.executable, *args], env=env)


def cmd_clone(args: list[str], prog: str) -> int:
    if len(args) > 2:
        panic(f"{prog}: clone: expected name and url to clone")
    name, args = shift(args)
    url, args = shift(args)
    if res := subprocess.call(["git", "clone", url, join(name)]):
        return res
    if "take.toml" not in os.listdir(join(name)):
        with open(join(name, "take.toml"), "w") as f:
            f.write(
                tomli_w.dumps(
                    {
                        "package": {
                            "name": name,
                            "version": input("What is the version? "),
                            "author": input("Who is the author? "),
                        },
                        "dependencies": {},
                    }
                )
            )


def cmd_reload(args: list[str], prog: str) -> int:
    os.chdir(join("take"))
    return main([__file__, "this", "install"])


def main(args: list[str]) -> int:
    prog, args = shift(args)
    if not os.path.isabs(prog):
        print(
            f"{prog}: warning: not calling from PATH. consider adding {join('take','bin')} to $PATH."
        )
    if len(args) < 1:
        panic(usage(prog))
    cmd, args = shift(args)

    builtincmds = {
        # (list[str], str) -> int
        "help": cmd_help,
        "new": cmd_new,
        "dbg": cmd_dbg,
        "this": cmd_this,
        "cc": cmd_cc,
        "py": cmd_py,
        "clone": cmd_clone,
        "reload": cmd_reload,
    }

    if cmd in builtincmds:
        return builtincmds[cmd](args, prog)
    else:
        panic(f"{prog}: {cmd}: invalid command")


if __name__ == "__main__":
    exit(main(sys.argv))
