#!/bin/bash

# Environment Name (Venv)
VENV_NAME="venv"

# Requirements File (optional)
REQUIREMENTS_FILE="requirements.txt"

# Function to check if python is callable
check_python() {
    if command -v python &> /dev/null; then
        return 0  # Python is found
    else
        return 1  # Python is not found
    fi
}

# Initial check for Python
if check_python; then
    echo "Python found. Proceeding..."
else
    echo "Python not found initially. Trying to activate Conda..."
    # Try activating Conda base environment
    if command -v conda &> /dev/null; then
        conda activate base
        # Check again for Python after activating Conda
        if check_python; then
            echo "Python found after activating Conda."
        else
            echo "Error: Python not found even after activating Conda."
            exit 1  # Exit with error code
        fi
    else
        echo "Error: Python not found, and Conda is not available."
        exit 1  # Exit with error code
    fi
fi

# Check if venv environment already exists
if [ -d $VENV_NAME ]; then
    echo "Virtual environment '$VENV_NAME' already exists. Skipping creation."

    # Activate the virtual environment
    source $VENV_NAME/bin/activate
else
    # Create the virtual environment 
    python3 -m venv $VENV_NAME
    echo "Virtual environment '$VENV_NAME' created."

    # Activate the virtual environment
    source $VENV_NAME/bin/activate

    # Install packages (if requirements file exists)
    if [ -f $REQUIREMENTS_FILE ]; then
        pip install -r $REQUIREMENTS_FILE
    fi
fi

# Success message
echo "Environment activated successfully!"
