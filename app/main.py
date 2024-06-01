import sys
import os

# Coloring for highlighting
RED = "\033[91m"
RESET = "\033[0m"


def echo(*args):
    print(" ".join(args))


def exit(*args):
    if len(args) == 0:
        print("Not enough arguments")
    elif str(args[0]) == "0":
        sys.exit()


def type(*args):
    if len(args) == 0:
        print("Not enough arguments")
        return

    command = args[0]
    if command in COMMANDS:
        print(f"{RED}{command}{RESET} is a shell {RED}builtin{RESET}")
        return

    command_path = search_executable(command)
    if command_path is not None:
        print(f"{RED}{command}{RESET} is {command_path}")
        return
    print(f"{command}: not found")


def search_executable(command):
    input_path = os.environ.get("PATH").split(":")
    for dir in input_path:
        command_path = os.path.join(dir, command)
        if os.path.isfile(command_path):
            if os.access(command_path, os.X_OK):
                return command_path
    return None


def pwd():
    print(os.getcwd())


def cd(*args):
    print("cd")


def execute_program(cmd, *args):
    command_path = search_executable(cmd)
    if command_path is not None:
        os.system(f"{command_path} {" ".join(args)}")
        return
    print(f"{cmd}: not found")


def default(command):
    command_path = search_executable(command)
    if command_path is None:
        print(f"{command}: {RED}command{RESET} not found")


# Available commands
COMMANDS = {
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
        command = input()
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
