import sys


RED = "\033[91m"
RESET = "\033[0m"
EXIT = "exit 0"


def main():
    command = ""
    while command != EXIT:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input()

        if command != EXIT:
            red_commmand = f"{RED}command{RESET}"
            print(f"{command}: {red_commmand} not found")


if __name__ == "__main__":
    main()
