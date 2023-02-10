# IPP 2023 Project Tests

# Description

This repository contains tests for the IPP 2023 project. The tests are located
in the `tests` directory. Each test case includes files with source
code (`*.src`), expected XML output (`*.xml`) and expected return
code (`*.code`).

# Usage

```bash
usage: main.py -i INTERPRET -s SOURCE [-f FILTER]

Testing tool for the first IPP Project

optional arguments:
  -i INTERPRET, --interpret INTERPRET
     PHP 8.1 interpreter
  -s SOURCE, --source SOURCE
     Path to parse.php file
  -f FILTER, --filter FILTER
     Filter tests by category. 
     Categories are divided by comma. 
     Categories can be any string contained in the test case path.
```

## Filtering

Filters are used to select only a subset of tests. The filter is a string
containing a comma-separated list of categories. The test case is selected if
its path contains any of the categories. The categories are case-sensitive.

| Filter                | Description                                      |
|-----------------------|--------------------------------------------------|
| `header`              | Selects only header tests                        |
| `good`                | Tests with expected return code 0                |
| `wrong`               | Tests with expected any return code other than 0 |
| `add`/`move`/`defvar` | Tests with the matching instruction              |

# Example

Selects all tests with the `good` and `header` categories and runs them.

```bash
python3 main.py -i php -s parse.php -f good,header
```

Selects all tests with the `good` category and runs them.

```bash
python3 main.py -i php -s parse.php -f good
```

Selects all tests with the `wrong` and `instruction` categories and runs them.

```bash
python3 main.py -i php -s parse.php -f wrong,instruction
```

# Contributing

Feel free to add more tests to this project 🧑‍💻.