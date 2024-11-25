#!/bin/bash

# Check if Poetry is installed
if command -v poetry > /dev/null 2>&1; then
    echo "Poetry is already installed!"
else
    # Installing Poetry
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "Poetry installed"

    # Export Poetry's PATH
    echo "Exporting Poetry's PATH..."
    export PATH="$HOME/.local/bin:$PATH"
fi

# Check poetry ver
poetry --version

# Configure virtual environment location and install dependencies
echo "Configuring virtual environment location and installing dependencies..."
poetry config virtualenvs.in-project true
poetry install --no-root

echo "Setup complete."
