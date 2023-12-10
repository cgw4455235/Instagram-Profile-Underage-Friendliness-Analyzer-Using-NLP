# Instagram Profile Underage Friendliness Analysis Tool
This README is the software documentation for this project.
# Video Presentation
[Please find video presentation here](https://veed.io/view/c5e12765-4de5-4cbb-8219-1db6b63aabfe)

# Overview of the Function of the code
This Python app can accept a user input for an Instagram profile username and collate scores to determine whether the profile contains violent themes, educational themes, and negative sentiment. Then, it will display those results on a simple UI for users to see the result of this analysis regarding whether this Instagram profile is age-appropriate. Generally-speaking, the app consists of low-intensity crawling functionalities, text-to-image conversion capabilities by leveraging pre-trained models, cosine similarity calculation between two vectors, and a simple user interface created with the Python `tk` library
 
# Implementation of Software
This app is generally implemented in the following manner:
1. It has a crawler functionality that leverages `Instaloader` library ([Link](https://instaloader.github.io/)) to create customized crawler logic. This custom crawler logic will download five posts from a targeted Instagram profile including text and images while excluding videos.
2.  After images and texts from the Instagram profile are downloaded, they're pre-processed via common Python libraries like nltk to remove stopwords. Then, images are converted into text descriptions via the `Salesforce/blip-image-captioning-large` ([Link](https://huggingface.co/Salesforce/blip-image-captioning-large)) pre-trained model.
3. Then, we would get sentence embeddings of those preprocessed text data via `code/topic_similarity.py` via the pre-trained `sentence-transformers/all-MiniLM-L6-v2` ([Link](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)) model. 
4. Then, the sentence embeddings are passed into a cosine similarity function called `torch.nn.CosineSimilarity` ([Link](https://pytorch.org/docs/stable/generated/torch.nn.CosineSimilarity.html)) between those sentence embeddings of the preprocessed Instagram post data and the sentence embeddings of the topical queries (i.e. educational topic and violent topic). We return the scores.
5. The next step is to obtain sentiment scores (i.e. postive, negative and neutral) by passing the preprocessed text sentences or descriptive sentences regarding the image from the Instagram profile to `finiteautomata/bertweet-base-sentiment-analysis` ([Link](https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis)) model, and we obtain the list of scores.
6. Finally, we obtain the highest scores for each sentiment and theme, then check if they have surpassed the baselines of those sentiments and themes, which are empirically determined via a set of collected 60 baseline Instagram profiles that have neutral sentiment and non-educational and non-violent themes. See ` code/utils/determine_underage_friendliness.py` and `code/generate_baseline_datasets_and_scores.py`. All the profiles used to establish the baseline are in this list `code/profile_data/baseline_profiles.py`
7. Display the analytical results via Python `tk` UI library and after comparing whether the scores have significantly surpassed their baseline scores.

## Future Works
It's recommended that to expand on this work, people can build features that are related to video content age appropriate evaluation features. 

## Code File and Purpose
### code/profile_data/baseline_profiles.py
This file contains all the 60 baseline Instagram profiles used to establish the baseline scores for each sentiment (i.e. positive, negative and neutral) and theme (i.e. violent and educational). 

### code/main.py
This file contains the actual logic for running the app for users to specify an Instagram profile. After the profile is specified, the Python app will download five posts from the Instagram profile and conduct theme and sentiment analysis by using pre-trained models to extract themes and sentiments from pictures and text posts of this profile to determine whether the profile contains violent themes, educational themes, and negative sentiment. When this function finishes running, it will display a simple UI to show the results of the analysis regarding what themes and sentiments this Instagram profile contains.
Please find instructions regarding how to use this app in the later section of this README.

### code/generate_baseline_datasets_and_scores.py
This file contains logic for establishing the baseline sentiment (i.e. positive, negative and neutral) scores and theme (i.e. violent and educational) scores by calculating sentiment and thematic scores on 60 Instagram profiles. Those baseline scores serve as the lowest threshold for determining whether a sentiment or theme exists in a Instagram text post or image post. This app calculates the sentiment and thematic score for all of these profiles and identify their averages, which will serve as the baseline scores. Then, it will save all the baseline data as pickle files in `code/baseline_scores`

### code/utils/constants.py
This file stores general constant variables like commonly used dictionary key names and sentiment labels.
### code/utils/crawler.py
This file contains Python code for extracting Instagram profiles' text and photo data and saving them on the local device.
### code/utils/determine_underage_friendliness.py
This file has logic that takes in the score of a sentiment analysis/thematic analysis on a text post or image post and determine whether this post contains a theme/sentiment.
### code/utils/img_to_text.py
This file converts an image to descriptive text.
### code/utils/process_data.py
 This file contains code to pre-process raw image and text data.
### code/utils/sentiment_analysis.py
This file contains code to analyze the sentiment from a text input, including negative, positive and neutral.
### code/utils/topic_similarity.py
This file contains to determine how similar a text input is to another text input
### code/utils/topic_types.py
This file contains constants about the thematic types this Python app can analyze, including violent and educational.   
### code/evaluate_effiacy.py
This file runs logic that evaluates whether the classifier works on a human selected set of profiles. It saves the result in a pickle file. We have 10 profiles each for negative sentiment, violence and education.
### code/baseline_scores
contains the baseline scores evaluated for the classifier that are collected from the 30 baseline profiles
### code/evaluation_scores
contains the final evaluation accuracy scores for the classifier 

# How to Use This Software
## Set Up Conda Environment
1. Install conda on your computer ([installation guide](https://conda.io/projects/conda/en/latest/user-guide/install/index.html))
2. Find the environment.yml and run the following command to create a python 3.9 Conda environment along with the necessary dependencies to run this Python app 
```python
conda env create -f environment.yml
``` 
3. then run `conda activate py39` . This will ready all the dependencies for you.
4. In your `~/zsh.rc` on Mac or a Windows/Linux equivalent, add `export PYTHONPATH="${PYTHONPATH}:[YOUR PATH]/cs410-final-proj/code` , so Python can find this package properly.
5. Clone this repo with `git clone https://github.com/cgw4455235/cs410-final-proj`

## Run an Instagram Profile Analysis
* Make sure you have a valid internet connection to access Hugging Face
* Under `code/main.py`, you can modify the Instagram profile you want to analyze by modifying the `profile_name` variable. You don't need to do anything else. 
* Then, run `main.py`directly via `python [PATH TO LOCAL CLONED REPO]/code/main.py`. If it succeeds, a simple UI will pop up on your screen to display the analysis results and samples of posts from the Instagram profile.
* adjust sensitivity via the `violent_check_threshold_sensitivity` and `educational_threshold_sensitivty` for topic evaluation

## Fix Instagram Connection Issue
* If there's an error from the code that says you cannot connect to Instagram, log into Instagram via Firefox
* then run `get_cookie.py` under `code/utils` to obtain a path to your cookie (it will print the path on the console of your code editor or terminal). The output portion that you need to copy would be something like `/Users/asddsa/.config/instaloader/session-acc_test_use`
* then find the path value in line 12 in `code/utils/crawler.py` and replace the example path value with this path value output from `get_cookie.py`. 

# Contribution of Each Team Member

This section describes the contribution of the team members. There is only one team member in this project (i.e. this team only consists of 1 person). This team member has done all the work in this project, including writing code, finding datasets, writing the project proposal, writing progress reports, creating software documentation, and creating the presentation video.


