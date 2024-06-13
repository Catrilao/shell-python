import subprocess
import sys
import os
from pathlib import Path
from typing import Any, Callable

# Coloring for highlighting
RED = "\033[91m"
RESET = "\033[0m"


def echo(*args: str) -> None:
    """Prints the arguments given."""
    print(" ".join(args))


def exit(*args: str) -> None:
    """Exit the program if the arguments is 0."""
    if len(args) == 0:
        print("Not enough arguments")
    elif str(args[0]) == "0":
        sys.exit()


def type(*args: str) -> None:
    """Prints the type of a given command."""
    if len(args) == 0:
        print("Not enough arguments")
        return

    command: str = args[0]
    if command in COMMANDS:
        print(f"{RED}{command}{RESET} is a shell {RED}builtin{RESET}")
        return

    command_path: str = search_executable(command)
    if command_path != "":
        print(f"{RED}{command}{RESET} is {command_path}")
        return

    print(f"{command}: not found")


def search_executable(command: str) -> str:
    """Search for an executable file in the system's PATH.

    Parameters
    ----------
    command : str
        The file that is to be searched.

    Returns
    -------
    str
        Path to the executable file if found, "" otherwise.
    """
    input_path: list[str] = os.environ.get("PATH", "").split(":")
    for dir in input_path:
        command_path: str = os.path.join(dir, command)
        if os.path.isfile(command_path):
            if os.access(command_path, os.X_OK):
                return command_path
    return ""


def pwd() -> None:
    """Prints the current working directory"""
    print(os.getcwd())


def cd(directory: str = "") -> None:
    """Goes to the specified directory, if not directory is given goes to home.

    Parameters
    ----------
    directory : str, optional
        Path to the given directory, by default ""
    """
    directory = directory.replace("~", str(Path.home()))

    if not directory:
        directory = str(Path.home())

    if not os.path.exists(directory):
        print(f"{directory}: No such {RED}file{RESET} or directory")
    elif os.access(directory, os.F_OK):
        os.chdir(directory)


def execute_program(cmd: str, *args: str) -> None:
    """Executes a program with the given arguments."""
    command_path: str = search_executable(cmd)
    if command_path != "":
        subprocess.run(f"{command_path} {' '.join(args)}")
        return
    print(f"{cmd}: not found")


def default(command: str) -> None:
    """Prints an error message if the command is not found.

    Parameters
    ----------
    command : str
        The command to be executed.
    """
    command_path: str = search_executable(command)
    if command_path == "":
        print(f"{command}: {RED}command{RESET} not found")


# Available commands
COMMANDS: dict[str, Callable[..., Any]] = {
    "echo": echo,
    "exit": exit,
    "type": type,
    "pwd": pwd,
    "cd": cd,
    "execute": execute_program,
    "default": default,
}


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command: str = input()
        cmd, *args = command.split()

        try:
            # Execute command
            COMMANDS[cmd](*args)
        except KeyError:
            if len(args) > 0:
                COMMANDS["execute"](cmd, *args)
            else:
                COMMANDS["default"](cmd)


if __name__ == "__main__":
    main()
