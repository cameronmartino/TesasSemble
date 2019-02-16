# TesasSemble
assemble in the 4th dimension 


### Environment

To install the conda environment, do

```
conda env create -f resources/environment.yml
```

Then activate the environment with ```conda activate tesas```.

Verify that the new environment was installed correctly with ```conda list```.

If you made any changes to the environment (e.g., pip install, conda install), then you need to save these changes to the environment; do

```
conda env export --no-builds | grep -v "prefix" > resources/environment.yml
```

For more [info](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

### Branching

For a more detailed explanation, see [this link](https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches).

First create a fork of the [repo](https://github.com/cameronmartino/TesasSemble), or make sure your master is up to date by runing ```git pull```

Then create the branch on your local machine and switch in this branch:

```
git checkout -b [name_of_your_new_branch]
```

Push the branch on github:

```
git push origin [name_of_your_new_branch]
```

Then you can commit and push as normal. When you have finalized the changes for the segment you are working on, navigate to the branch of your forked repo on the github website and submit a Pull request.



### Testing

To run unit tests (locally from the outer ```TesasSemble``` directory), do

```bash
py.test test
```
