# Hornets Python Template

This is the template GitHub project for our group.

## Getting started

1. Use this template:
	- New project: select **Use this template > Create a new repository**.
	- Existing project: clone this repository and copy all the files of this repository, except the `README.md`, to your own project. If you already have existing files with the same name, check what you want to take over.
1. Open the `conda.yml` file and change the `name` on line 1. The name is the name of your virtual environment. Add the python version at the end of the virtual environment name to show the python version. Thus if you use Python 3.9 your environment name is `myproject39`, if you use Python 3.10 it is `myproject310`.
1. Open the `pyproject.toml` and change:
    - under `[project]` the `name` to your project name. Here do not add the python version.
    - `authors` change the placeholder `Your Name` to your own name and change the email address.
1. Then run the following commands
   ```bash
   conda env create -f conda.yml # creates a new virtual environment according to the conda.yml file
   conda activate <myproject> # Activates your newly created project. Make sure to replace <myproject> with the project name you set in the conda.yml
   hatch env create # Installs all the dependencies listed in the pyproject.toml
   pre-commit install # Sets up pre-commits, which correct the formatting of your files among other things.
   ```

## Installing a new python module

To install a new python package, for example `hat-creaform`, add it as a dependency inside the `pyproject.toml`:

```diff
[project]
...
dependencies = [
    "hat-docs",
+   "hat-creaform"
]
...
```

And reload the environment. This automatically installs the added packages from the `pyproject.toml`:

    hatch env create
