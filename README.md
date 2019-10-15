# Resource Checker Tool.

Tool to check where URL leads after all redirects. And also to check if there is no troublesome situations with this URL: like a cyclic redirects or an endless content.

## Install

Prepare your environment. For example if your choice is [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/):
```bash
cd dir_with_project
mkvirtualenv -a . --python=python3.7 url_checker
workon url_checker
```
Install requirements (inside your `dir_with_project`):
```bash
pip install -r requirements.txt
```

## Test

Now you can run unit tests (powered with pytest):
```bash
pip install -e '.[test]'
pytest
```

Or you can run test server and then check it with CLI tool:
```bash
python -m test_server -H localhost -P 8080
```

## Use

Here will be the manual for a CLI tool.