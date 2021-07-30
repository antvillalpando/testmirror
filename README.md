# WP6

## Jupyter notebooks

The `misc/notebooks` directory contains examples demonstrating how the quantum
and classical NLP modules are used to solve NLP-related problems (currently – a
sentence classification task).

### Setup
To run the notebooks you must install some software dependencies and download a
`spacy` language model.

#### Dependencies
We recommend using `virtualenv` or `anaconda` to create a isolated environment
for the project's dependencies. Here are instructions for `virtualenv`.

```sh
# Install virtualenv using your distributions package manager or pip, e.g.,
apt install virtualenv  # if using Ubuntu

# Create a new virtual environment called, e.g., venv.
# This will create a directory called venv in the project root which will
# contain all of the packages installed in the following steps. It can be safelly
# delted to get rid of the these packages.
virtualenv create venv

# Activate the newly created environment
. ./venv/bin/activate

# Install the dependencies into the virtual environment
pip install -r requirements.txt
```

##### A note on the Python version
We've tested that the code works using Python 3.9. Earlier versions might not
work on Linux due to incompatibility with `myqlm`.

#### Spacy language model
Some of the tools used in the code require a language model to be downloaded to
the users system. To do it automatically, execute the following command into the
virtual environment after the dependencies have been installed (see the
Dependencies section above).

```sh
# Make sure the virtual environement is activated
. ./venv/bin/activate

# The language model will be stored in the venv directory
python -m spacy download en_core_web_lg
```

### Running
To run the the notebooks, start jupyter lab and navigate to the notebooks in
[misc/notebooks/](./misc/notebooks/)

```sh
# Make sure the virtual environement is activated
. ./venv/bin/activate

# Start jupyter lab and follow the instructions in the console
# output to open jupyter lab in the browser
jupyter-lab
```

### More information
Some more information about the notebooks is provided in
[misc/notebooks/README.md](./misc/notebooks/README.md)

## Generating the animal dataset
Manual dataset generation isn't necessary for running the Jupyter notebooks.
However, if needed for some different purpose, the dataset can be generated
using the following commands.

Run
```sh
./src/gen-animal-dataset.py --seed 1337 > outfile
```
to generate a tab-separated file containing lines of the form
`<sentence>\t<sentence_type>\t<truth_value>` where `<truth_value>` is 1 if the sentence states a
fact that is true and 0 otherwise, and `<sentence_type>` denotes the sentence type, e.g., `NOUN-TVERB-NOUN`.

# NEASQC lib template

This repository is a template for NEASQC libraries.

## Licence

The `LICENCE` file contains the default licence statement as specified in the proposal and partner agreement.

## Building and installing

For simplicity, an example of `setup.py` file is provided in this template.
Feel free to modify it if you have exotic build recipes.


## Coding conventions

In order to simplify the coding conventions, we provide a pylint.rc file in `misc/pylint.rc`.
This will allow you to easily check your naming conventions and various other aspects.
This is not a strict guidline, as pylint can be quite pedantic sometimes (but also very helpful).

A few remarks:
- pylint can be integrated in most editors (and we strongly advise you to)
- running pylint on several source files in one go can find errors such as circular imports or code duplication:

```bash
python -m pylint --rcfile=./misc/pylint.rc <my_source_dir>
```
or

```bash
pylint --rcfile=./misc/pylint.rc <my_source_dir>
```

depending on how you installed pylint.

## Testing and continuous integration

In order to uniformise the continuous integration process across libraries, we will assume that:
- all the tests related to your library are compatible with pytest
- there exists a 'test' recipe in the `setup.py` file

The default test recipe (in this template) simply calls pytest on the full repository.
Pytest detects:
- any file that starts with test\_ (e.g test\_my\_class.py)
- inside these files, any function that starts test\_
- any class that starts with Test

You can run it with:

```bash
python setup.py test
```

This way, you can write tests either right next to the corresponding code (convenient) or in a `tests` folder at the root of the repository.

If you are not familiar with unit testing and you feel that it's too much for your project, that's fine.
The bare minimum would be to include some run examples wrapped in test functions (functional tests).

Remark that in this template, the same tests are in my\_lib/test\_my\_lib.py and tests/test\_my\_lib.py.

## GitHub CI
This repository contains a GitHub Workflow file that will automatically run pytest when changes are pushed.  
Details on disabling and enabling this feature can be found [here](https://docs.github.com/en/enterprise-server@3.0/actions/managing-workflow-runs/disabling-and-enabling-a-workflow).
