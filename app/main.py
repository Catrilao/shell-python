import subprocess
import sys
import os
from pathlib import Path
from typing import Any, Callable

# Coloring for highlighting
RED = "\033[91m"
RESET = "\033[0m"


def echo(*args: str) -> None:
    print(" ".join(args))


def exit(*args: str) -> None:
    if len(args) == 0:
        print("Not enough arguments")
    elif str(args[0]) == "0":
        sys.exit()


def type(*args: str) -> None:
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
    input_path: list[str] = os.environ.get("PATH", "").split(":")
    for dir in input_path:
        command_path: str = os.path.join(dir, command)
        if os.path.isfile(command_path):
            if os.access(command_path, os.X_OK):
                return command_path
    return ""


def pwd() -> None:
    print(os.getcwd())


def cd(directory: str = "") -> None:
    directory = directory.replace("~", str(Path.home()))

    if not directory:
        directory = str(Path.home())

    if not os.path.exists(directory):
        print(f"{directory}: No such {RED}file{RESET} or directory")
    elif os.access(directory, os.F_OK):
        os.chdir(directory)


def execute_program(cmd: str, *args: str) -> None:
    command_path: str = search_executable(cmd)
    if command_path != "":
        subprocess.run(f"{command_path} {' '.join(args)}")
        return
    print(f"{cmd}: not found")


def default(command: str) -> None:
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
