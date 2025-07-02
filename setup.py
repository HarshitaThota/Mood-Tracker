from setuptools import setup, find_packages

setup(
    name="mood-tracker",            # The package name (also how it’ll appear on PyPI)
    version="0.1.0",                # Your release version
    packages=find_packages(),       # Auto-discovers all sub-packages in `app/`
    install_requires=["click"],     # External deps: here we depend on Click for the CLI
    entry_points={
        "console_scripts": [
            # Exposes the `cli()` function in app/cli.py as the `mood` command
            "mood=app.cli:cli"
        ]
    },
)


# In practice, running pip install . in your project root will:

# Install Click (and any other required libraries).

# Copy your app/ code into the environment’s site-packages so Python can import it.

# Generate a mood executable in the environment’s bin/Scripts folder—letting
# anyone call mood add, mood list, etc., just like any other CLI tool.