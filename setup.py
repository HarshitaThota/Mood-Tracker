from setuptools import setup, find_packages

setup(
    name="mood-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            # this is the magic that makes `mood` show up
            "mood=app.cli:cli"
        ]
    },
)
