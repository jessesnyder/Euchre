# Euchre
This is my Euchre program.

## Developer installation

    pip install -r dev-requirements.txt
    pip install --editable .
    pre-commit install

## Running tests

### Just the tests

    pytest

### Tests, with coverage

    coverage run euchre_env/bin/pytest; coverage report; coverage html

then,

    open htmlcov/index.html
