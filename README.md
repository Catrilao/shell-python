# Python Shell Implementation

[![progress-banner](https://backend.codecrafters.io/progress/shell/dbbe392b-b16f-4fc5-bfab-3cd771d83ecb)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This project is part of the ["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview) by Codecrafters. Through this challenge, I’ve explored the fundamentals of Unix-like shell environments and implemented various features to bring this shell to life.

## Project Overview

In this project, I've developed a basic shell that can handle built-in commands such as `cd`, `echo`, `pwd`, `type`, and also execute external programs found in the system’s `PATH`. Here are some of the key capabilities and features I’ve added:

- **Built-in Commands**: Support for essential shell commands.
- **External Program Execution**: Running external binaries and scripts.
- **Command History**: Maintaining a session's command history and enabling auto-completion.
- **Error Handling**: Graceful handling of various error scenarios to ensure smooth operation.

## Features I Implemented

1. **Command History and Auto-completion**:

   - I set up command history using Python's `readline` module.
   - Implemented auto-completion for commands, making the shell more user-friendly.

2. **Built-in Commands**:

   - **`echo`**: Prints the provided arguments.
   - **`pwd`**: Displays the current working directory.
   - **`cd`**: Changes the working directory.
   - **`type`**: Checks if a command is built-in or an external executable.
   - **`exit`**: Exits the shell and saves the command history.

3. **External Program Execution**:

   - My shell can search for and execute external programs, similar to how traditional shells operate.

4. **Robust Error Handling**:
   - Implemented comprehensive error handling for file operations and command executions to provide meaningful feedback to the user.

## How to Use This Shell

### Prerequisites

- Python 3.11 or higher.

### Running the Shell

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/catrilao/shell-python.git
   cd shell-python
   ```

2. **Start the Shell**:

   ```sh
   ./your_shell.sh
   ```

3. **Try It Out**:
   Once the shell is running, you can enter commands as you would in any terminal. Here are some commands you can try:
   ```sh
   $ echo "Hello from my custom shell!"
   $ pwd
   $ cd /some/directory
   $ type ls
   $ ls -la
   $ exit
   ```

### Example Commands

- **`echo Hello, World!`**: Prints `Hello, World!`.
- **`pwd`**: Shows the current working directory.
- **`cd ~`**: Changes to the home directory.
- **`type ls`**: Checks if `ls` is a built-in command or an external program.
- **`exit`**: Exits the shell and saves the command history.

## Development Process

This project has been a fantastic learning experience. I’ve enjoyed diving into the internals of shell operations and translating those concepts into Python code. Here’s a brief overview of how I developed and tested each feature:

1. **Initial Setup**:

   - Started by setting up a basic loop to read and execute commands.
   - Implemented support for simple built-in commands.

2. **Adding Functionality**:

   - Expanded support to handle external commands using Python’s `subprocess` module.
   - Enhanced the shell with command history and auto-completion.

3. **Robust Error Handling**:

   - Added comprehensive error handling to provide clear feedback and maintain smooth operation.

4. **Testing and Refinement**:
   - Manually tested each feature to ensure proper functionality.
   - Refined command parsing and error messages for better user experience.

## Acknowledgments

- **Codecrafters**: Thanks to Codecrafters for providing the "Build Your Own Shell" challenge. It has been instrumental in enhancing my skills in shell environments and Python programming.
