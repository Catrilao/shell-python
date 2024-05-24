import sys

# Coloring for highlighting
RED = "\033[91m"
RESET = "\033[0m"


def echo(*args):
    print("".join(" ".join(args)))


def exit(*args):
    if len(args) == 0:
        print("Not enough arguments")
    elif str(args[0]) == "0":
        sys.exit()


def type(*args):
    if len(args) == 0:
        print("Not enough arguments")
    elif args[0] in COMMANDS:
        command = f"{RED}{args[0]}{RESET}"
        builtin = f"{RED}builtin{RESET}"
        print(f"{command} is a shell {builtin}")
    else:
        print(f"{args[0]} not found")


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
