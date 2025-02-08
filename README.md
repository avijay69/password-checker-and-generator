# Password Checker and Generator

A Python-based tool that provides two essential functionalities: generating secure, random passwords and checking the strength of your existing passwords. This project is designed with simplicity and security in mind, making it easy to create and evaluate passwords from the command line.

## Features

- **Password Generator:**  
  Create strong, random passwords with customizable options such as length and character sets (uppercase, lowercase, digits, and symbols).

- **Password Checker:**  
  Evaluate the strength and security of a given password by checking for complexity, common vulnerabilities, and adherence to best practices.

- **Easy to Use:**  
  Run either functionality directly from the command line with clear instructions.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/avijay69/password-checker-and-generator.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd password-checker-and-generator
   ```

3. **(Optional) Create and Activate a Virtual Environment:**

   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

4. **Install the Required Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

The project is divided into two main components: the password checker and the password generator. Use the commands below to run each tool.

- **Password Checker:**

  ```bash
  python password_checker/main.py
  ```

- **Password Generator:**

  ```bash
  python password_generator/main.py
  ```

*Note: Adjust the file paths if your project structure changes.*

## Project Structure

```
password-checker-and-generator/
├── assets/             # (Optional) Images or other asset files
├── build/              # Build-related files and scripts
├── dist/               # Distribution packages or compiled files
├── src/                # Core source code (if applicable)
├── password_checker/   # Password checker module and scripts
├── password_generator/ # Password generator module and scripts
├── requirements.txt    # Python dependencies list
├── README.md           # This documentation file
└── venv/               # Virtual environment folder (if created)
```

## Contributing

Contributions are welcome! If you have suggestions, bug fixes, or new features, please feel free to fork the repository and submit a pull request. When contributing, please adhere to the existing code style and include tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, issues, or suggestions, please open an issue in the repository or contact the repository owner.
