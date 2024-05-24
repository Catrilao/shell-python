import sys


RED = "\033[91m"
RESET = "\033[0m"


def main():
    sys.stdout.write("$ ")
    sys.stdout.flush()

    # Wait for user input
    command = input()
    red_commmand = f"{RED}command{RESET}"
    print(f"{command}: {red_commmand} not found")


if __name__ == "__main__":
    main()
