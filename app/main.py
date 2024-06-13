import readline
import subprocess
import sys
import os
from pathlib import Path
from typing import Any, Callable

# Coloring for highlighting
RED = "\033[91m"
RESET = "\033[0m"

# Command history and auto-completion setup
readline.parse_and_bind("tab: complete")
history_file: str = os.path.expanduser("~/.pysh_history")


def load_history():
    """Load command history from the history file if it exists."""
    if os.path.exists(history_file):
        readline.read_history_file(history_file)


def save_history():
    """Save the current session's command history to the history file."""
    readline.write_history_file(history_file)


load_history()


def echo(*args: str) -> None:
    """Prints the arguments given."""
    print(" ".join(args))


def exit_shell(*args: str) -> None:
    """Exit the program."""
    save_history()
    sys.exit()


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


def pwd() -> None:
    """Prints the current working directory"""
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


def execute_program(cmd: str, *args: str) -> None:
    """Executes a program with the given arguments."""
    input_path: list[str] = os.environ.get("PATH", "").split(":")
    for dir in input_path:
        command_path: str = os.path.join(dir, cmd)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            try:
                subprocess.run([command_path, *args])
            except FileNotFoundError:
                print(f"File '{' '.join(args)}' not found")
            return

    print(f"{cmd}: not found")


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

            cmd, *args = command.split()

            if cmd in COMMANDS:
                # Execute command
                COMMANDS[cmd](*args)
            else:
                COMMANDS["default"](cmd, *args)
        except KeyboardInterrupt:
            print("Type 'exit'  to quit.")
        except EOFError:
            exit()


if __name__ == "__main__":
    main()
