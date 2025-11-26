# Contributing

First off, thanks for taking the time to contribute! 🚀

Welcome all contributions from the community to help improve this project.

## How to Contribute

### Reporting Bugs
If you find a bug or unexpected behavior, please open an issue on GitHub.
* Check if the issue already exists.
* Provide as much detail as possible (OS, version, steps to reproduce).

### Requesting Features
Have an idea for a new feature or improvement?
* Open a Feature Request ticket.
* Describe *why* this feature would be useful.

### Submitting Changes (Pull Requests)

1.  **Fork the Repo**: Click the "Fork" button in the top right corner.
2.  **Clone your Fork**:
    ```bash
    git clone https://github.com/YOUR-USERNAME/mail-ops-scripts.git
    ```
3.  **Create a Branch**:
    ```bash
    git checkout -b my-new-feature
    ```
4.  **Make your Changes**: Edit the code and save.
5.  **Test Your Changes**: Ensure everything runs as expected.
6.  **Push and PR**: Push your branch to your fork and open a Pull Request against the `main` branch.

### Python Development Guidelines
I aim for clean, modern, and portable Python code.

* **Standard Library Only**: This project strives to have **zero external dependencies** to ensure maximum portability. Please avoid adding `pip install` requirements unless absolutely necessary and discussed in an issue first.
* **Style & Formatting**:
    * We follow [PEP 8](https://peps.python.org/pep-0008/) guidelines.
    * Code should be formatted using **Black** or similar auto-formatters.
    * Use 4 spaces for indentation.
* **Type Hinting**: We encourage modern Python type hints (e.g., `def my_func(name: str) -> bool:`) to improve readability and tooling support.
* **Linting**: We recommend running `flake8` or `ruff` locally to catch syntax errors and undefined variables before pushing.

## License

By contributing, you agree that your contributions will be licensed under the project's license.