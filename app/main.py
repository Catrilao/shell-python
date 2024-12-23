import re
import subprocess
import sys
import os
from pathlib import Path
from typing import Any, Callable

# Coloring for highlighting
RED = "\033[91m"
RESET = "\033[0m"


def echo(args: str) -> None:
    """Prints the arguments given."""
    kwargs = ""
    args_stripped = args.strip()

    pattern = r"('([^']*)'|\"([^\"]*)\")|[^'\" ]+"
    groups_args = re.finditer(pattern, args_stripped)

    for match in groups_args:
        group = match.group(0)

        if group.startswith("'") and group.endswith("'"):
            kwargs += " " + group.strip("'")
            continue

        if group.startswith('"') and group.endswith('"'):
            kwargs += " " + group.strip('"')
            continue

        for word in group.split():
            kwargs += " " + word.replace("\\", "")

    print(kwargs.removeprefix(" "))


def exit_shell(args: str) -> None:
    """Exit the program."""
    if len(args) == 0:
        print("Use: exit <code>")
        return
    sys.exit(int(args))


def type_shell(*args: str) -> None:
    """Prints the type of a given command."""
    if len(args) == 0:
        print("Not enough arguments")
        return

    command: str = args[0]
    if command in COMMANDS:
        print(f"{RED}{command}{RESET} is a shell {RED}builtin{RESET}")
        return

    input_path: list[str] = os.environ.get("PATH", "").split(":")
    for dir in input_path:
        command_path: str = os.path.join(dir, command)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            print(f"{RED}{command}{RESET} is {command_path}")
            return

    print(f"{command}: not found")


def pwd(args: str) -> None:
    """Prints the current working directory"""
    if len(args) > 0:
        print(f"{RED}pwd{RESET}: too many arguments")
        return
    print(os.getcwd())


def cd(directory: str = "") -> None:
    """Change to the specified directory, or home if none is specified.

    Parameters
    ----------
    directory : str, optional
        Path to the given directory, by default ""
    """
    directory = directory.replace("~", str(Path.home()))

    if not directory:
        directory = str(Path.home())

    try:
        os.chdir(directory)
    except FileNotFoundError:
        print(f"{directory}: No such {RED}file{RESET} or directory")
    except PermissionError:
        print(f"{directory}: {RED}Permission{RESET} denied")
    except Exception as e:
        print(f"Error changing directory: {e}")


def execute_program(cmd: str, args: str) -> None:
    """Executes a program with the given arguments.

    Parameters
    ----------
    cmd : str
        Command that is going to be executed.

    args : list[str], optional
        Arguments of the command.
    """
    input_path: list[str] = os.environ.get("PATH", "").split(":")
    for dir in input_path:
        command_path: str = os.path.join(dir, cmd)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            args_stripped = args.strip()
            pattern = r"('([^']*)'|\"([^\"]*)\")|[^'\" ]+"
            groups_args = re.finditer(pattern, args_stripped)
            kwargs = ""

            for match in groups_args:
                group = match.group(0)

                if group.isspace() or len(group) == 0:
                    continue

                kwargs = group

                if group.startswith("'") and group.endswith("'"):
                    kwargs = group.strip("'")
                elif group.startswith('"') and group.endswith('"'):
                    kwargs = group.strip('"')

                try:
                    subprocess.run([command_path, kwargs])
                except FileNotFoundError:
                    print(f"File '{' '.join(kwargs)}' not found")
            return

    print(f"{cmd}: command not found")


# Available commands
COMMANDS: dict[str, Callable[..., Any]] = {
    "echo": echo,
    "exit": exit_shell,
    "type": type_shell,
    "pwd": pwd,
    "cd": cd,
    "default": execute_program,
}


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            # Wait for user input
            command: str = input()

            if not command:
                continue

            cmd, _, args = command.partition(" ")

            if cmd in COMMANDS:
                COMMANDS[cmd](args)
            else:
                COMMANDS["default"](cmd, args)
        except KeyboardInterrupt:
            print("Type 'exit'  to quit.")
        except EOFError:
            exit()


if __name__ == "__main__":
    main()
