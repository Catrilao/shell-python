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
    else:
        input_path = os.environ.get("PATH").split(":")
        for dir in input_path:
            command_path = os.path.join(dir, command)
            if os.path.isfile(command_path):
                if os.access(command_path, os.X_OK):
                    print(f"{RED}{command}{RESET} is {command_path}")
                return
        print(f"{command}: not found")


# Available commands
COMMANDS = {
    "echo": echo,
    "exit": exit,
    "type": type,
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
            # Command not found
            red_commmand = f"{RED}command{RESET}"
            print(f"{cmd}: {red_commmand} not found")


if __name__ == "__main__":
    main()
