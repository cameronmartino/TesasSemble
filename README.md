[![Build Status](https://travis-ci.org/cameronmartino/TesasSemble.svg?branch=master)](https://travis-ci.org/cameronmartino/TesasSemble)
[![Coverage Status](https://coveralls.io/repos/github/cameronmartino/TesasSemble/badge.svg?branch=master)](https://coveralls.io/github/cameronmartino/TesasSemble?branch=master)

# TesasSemble
assemble in the 4th dimension 


### Environment

To install the conda environment, do

```bash
conda env create -n tesas --file resources/environment.yml
```

Then activate the environment with ```conda activate tesas```.

Verify that the new environment was installed correctly with ```conda info --envs```.

If you made any changes to the environment (e.g., pip install, conda install), then you need to save these changes to the environment; do

```bash
conda env export --no-builds | grep -v "prefix" > resources/environment.yml
```

If you need to pip install a package, you must use your environment's version of pip, i.e., do not just ```pip install```, do
```bash
[/path/to/your/conda/envs]/tesas/bin/pip install [package_name]
```

This will make sure conda is managing the packages you install with pip. More concretely, this should look something like

```bash
/Users/jdoe/miniconda3/envs/tesas/bin/pip install numpy
```

If you write something that depends on a package that you pip/conda install, make sure to export your environment and commiti the resources/environment.yml file.

For more [info](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

### Branching

For a more detailed explanation, see [this link](https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches).

First create a fork of the [repo](https://github.com/cameronmartino/TesasSemble), or make sure your master is up to date by runing ```git pull```

Then create the branch on your local machine and switch in this branch:

```
git checkout -b [name_of_your_new_branch]
```

Push the branch on github and set the remote as upstream:

```
git push --set-upstream origin [name_of_your_new_branch]
```

Then you can commit and push as normal. When you have finalized the changes for the segment you are working on, navigate to the branch of your forked repo on the github website and submit a Pull request.

Other helpful links:
[Sync a fork of a repository to keep it up-to-date with the upstream repository](https://help.github.com/articles/syncing-a-fork/)

[Configuring a remote fork](https://help.github.com/articles/configuring-a-remote-for-a-fork/)

[Pull from master into development branch](https://stackoverflow.com/questions/20101994/git-pull-from-master-into-the-development-branch/20103414)

[How to revert a Git repository to a previous commit](https://stackoverflow.com/questions/4114095/how-to-revert-a-git-repository-to-a-previous-commit)

[Branch from a previous commit using Git](https://stackoverflow.com/questions/2816715/branch-from-a-previous-commit-using-git)

[Using the github UI](https://guides.github.com/activities/hello-world/)

### Testing
To run unit tests (locally from the outer ```TesasSemble``` directory), do

```bash
nosetests -v tests --with-coverage --cover-package=TesasSemble
```

```bash
flake8 TesasSemble
flake8 test
```
## Benchmarks

All benchmarking results and data can be found in [TesasSemble-benchmarking](https://github.com/cameronmartino/TesasSemble-benchmarking)
