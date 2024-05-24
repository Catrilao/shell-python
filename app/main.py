import sys

# Coloring for the command not found error
RED = "\033[91m"
RESET = "\033[0m"


def echo(*args):
    print("".join(" ".join(args)))


def exit(*args):
    if len(args) == 0:
        print("Not enough arguments")
    elif int(args[0]) == 0:
        sys.exit()


# Available commands
COMMANDS = {
    "echo": echo,
    "exit": exit,
}


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input()

        try:
            # Execute command
            cmd, *args = command.split()
            COMMANDS[cmd](*args)
        except KeyError:
            # Command not found
            red_commmand = f"{RED}command{RESET}"
            print(f"{command}: {red_commmand} not found")


if __name__ == "__main__":
    main()
