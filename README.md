# 2FA Authenticator

This Python script provides a command-line based Two-Factor Authentication (2FA) tool using the HMAC-based One-Time Password (HOTP) and Time-Based One-Time Password (TOTP) algorithms. It allows you to generate OTPs, manage your secrets, and display the codes using a curses-based UI.

## Features

- Generate HOTP and TOTP codes
- Save and load secrets to/from a JSON file
- Normalize secret format
- Add, delete, and move codes
- Display codes in a curses-based UI

## Requirements

- Python 3.x
- `curses` module (should be included with most Python installations)
- `hmac`, `base64`, `struct`, `hashlib`, `os`, `json`, `re`, and `time` modules (standard libraries)

## Usage

1. **Clone the repository:**

    ```sh
    git clone https://github.com/maxbybee/python-authy.git
    cd python-authy
    ```

2. **Run the script:**

    ```sh
    python authenticator.py
    ```

3. **Interact with the UI:**

    - **Add code:** Enter the base32 encoded secret and a nickname for the code.
    - **Delete code:** Enter the index of the code to delete.
    - **Move code:** Enter the old index, new index, and optionally a new nickname.
    - **Exit:** Quit the program.

## Code Explanation

### Functions

- **`generate_hotp(secret, counter, digits=6)`**
  - Generates an OTP using the HMAC-based One-Time Password algorithm.
  - `secret`: The shared secret key.
  - `counter`: The counter value.
  - `digits`: The number of digits in the OTP (default is 6).

- **`generate_totp(secret, interval=30, digits=6)`**
  - Generates a TOTP using the Time-Based One-Time Password algorithm.
  - `secret`: The shared secret key.
  - `interval`: The time interval in seconds (default is 30).
  - `digits`: The number of digits in the OTP (default is 6).

- **`save_secrets(secrets)`**
  - Saves the list of secrets to a `secrets.json` file.

- **`load_secrets()`**
  - Loads the list of secrets from a `secrets.json` file.

- **`normalize_secret(secret)`**
  - Normalizes the format of a secret key.

### Classes

- **`Authenticator`**
  - Manages the 2FA authenticator.
  - Methods:
    - `__init__()`: Initializes the authenticator and loads secrets.
    - `add_code(secret, nickname)`: Adds a new code.
    - `delete_code(index)`: Deletes a code by index.
    - `move_code(old_index, new_index, new_nickname)`: Moves a code to a new index and optionally changes its nickname.
    - `display_codes(stdscr)`: Displays the codes in a curses-based UI.
    - `run(stdscr)`: Runs the main loop for the curses-based UI.

### Main Execution

- **`main(stdscr)`**
  - Initializes the `Authenticator` and starts the curses UI.

- **`wrapper(main)`**
  - Wraps the `main` function to initialize the curses application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## Acknowledgments

- Inspired by the need for a simple, command-line based 2FA tool.

