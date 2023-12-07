# Instagram Profile Underage Friendliness Analysis Tool

This Python app conducts

1) An overview of the function of the code (i.e., what it does and what it can be used for). 

2) Documentation of how the software is implemented with sufficient detail so that others can have a basic understanding of your code for future extension or any further improvement. 

3) Documentation of the usage of the software including either documentation of usages of APIs or detailed instructions on how to install and run a software, whichever is applicable. 

# How to Use This Software
## Set Up Conda Environment
1. Install conda on your computer ([installation guide](https://conda.io/projects/conda/en/latest/user-guide/install/index.html))
2. Find the environment.yml and run
```python
conda env create -f environment.yml
``` 
3. then run `conda activate py39` . This will ready all the dependencies for you.
4. In your `~/zsh.rc` on Mac or a Windows/Linux equivalent, add `export PYTHONPATH="${PYTHONPATH}:[Your PATH]/proj/underage_instagram_friendliness` , so Python can find this package properly.

## Run an Instagram Profile Analysis
under `code/main.py`, you can modify the Instagram profile you want to analyze by modifying the `profile_name` variable. You don't need to do anything else. Then, run `main.py`directly. If it succeeds, a simple UI will pop up on your screen to display the analysis results and samples of posts from the Instagram profile.

## Fix Instagram Connection Issue
if there's an error from the code that says you cannot connect to Instagram, log into Instagram via Firefox, then run `get_cookie.py` under `code/utils` to obtain a path to your cookie (it will print the path on the console of your code editor or terminal), then find the path value in line 12 in `code/utils/crawler.py` and replace the example path value with this path value output from `get_cookie.py`. 

# Contribution of Each Team Member

This section describes the contribution of the team members. There is only one team member in this project (i.e. this team only consists of 1 person). This team member has done all the work in this project, including writing code, finding datasets, writing the project proposal, writing progress reports, creating software documentation, and creating the presentation video.


