import re
import subprocess
import sys
import os
from pathlib import Path
from typing import Any, Callable


def echo(raw_input: str) -> None:
    """Prints the arguments given."""
    result = ""
    pattern = r"('([^']*)'|\"([^\"]*)\"+\s?)|(\S+\s?)"
    matches = re.finditer(pattern, raw_input.strip())

    for match in matches:
        group = match.group(0)

        if group.startswith("'") and group.endswith("'"):
            result += group.strip("'")
            continue

        idx = 0
        is_escape_char = True
        while idx < len(group):
            if group[idx] in ["\\", '"']:
                if group[idx - 1] == "\\" and is_escape_char and idx != 0:
                    result += group[idx]
                    if group[idx] == "\\":
                        is_escape_char = False
                idx += 1
                continue

            result += group[idx]
            idx += 1

    print(result)


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
        print(f"{command} is a shell builtin")
        return

    input_path: list[str] = os.environ.get("PATH", "").split(":")
    for dir in input_path:
        command_path: str = os.path.join(dir, command)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            print(f"{command} is {command_path}")
            return

    print(f"{command}: not found")


def pwd(args: str) -> None:
    """Prints the current working directory"""
    if len(args) > 0:
        print("pwd: too many arguments")
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
        print(f"{directory}: No such file or directory")
    except PermissionError:
        print(f"{directory}: Permission denied")
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
    search_path: list[str] = os.environ.get("PATH", "").split(":")

    for dir in search_path:
        executable: str = os.path.join(dir, cmd)

        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            pattern = r"('([^']*)'|\"([^\"]*)\")|[^'\" ]+"
            matches = re.finditer(pattern, args.strip())
            current_argument = ""

            for match in matches:
                group = match.group(0)

                if group.isspace() or len(group) == 0:
                    continue

                current_argument = group

                if group.startswith("'") and group.endswith("'"):
                    current_argument = group.strip("'")
                elif group.startswith('"') and group.endswith('"'):
                    current_argument = group.strip('"')

                try:
                    subprocess.run([executable, current_argument])
                except FileNotFoundError:
                    print(f"File '{' '.join(current_argument)}' not found")
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

            pattern = r"('([^']*)'|\"([^\"]*)\"|([^'\"\s]+))"
            match = re.match(pattern, command).group(0)
            separator = match

            if match.startswith("'") and match.endswith("'"):
                separator = match.strip("'")
            elif match.startswith('"') and match.endswith('"'):
                separator = match.strip('"')

            _, cmd, args = command.partition(separator)

            if cmd in COMMANDS:
                COMMANDS[cmd](args.strip())
            else:
                COMMANDS["default"](cmd, args.strip())
        except KeyboardInterrupt:
            print("Type 'exit'  to quit.")
        except EOFError:
            exit()


if __name__ == "__main__":
    main()
