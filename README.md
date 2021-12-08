# README
## Introduction
The purpose of this project was to create a covid dashboard that makes use of live API data.
The project takes live API data such as number of deaths, number of current hospital cases and
the 7 day infection rate for both local and national locations specified in the config file.
The project also takes live covid news articles and displays those articles with the title,
a small part of the content and a link to the rest of the article.
the project also uses schedualing to schedule updates for a specified time that can occur once 
or repeatidly at that time, as well as being either a news update or a data update.

## Prerequisites
python 3.10

## Installation
pip install -r requirements

## Getting Started Tutorial

### Setting Up and Accessing Dashboard

1. go to news api.org and get your API key.

2. Input your nation e.g. England, local location e.g Exeter, search terms e.g. covid and news API 
key into the config_template.json then rename config_template.json to config.json.

3. Run flask module 

4. input the IP address and port number of the dashboard into a browser (127.0.0.1:5000) 

### Using Dashboard

If set up correctly you should see a dashboard with an empty list of scheduled updates on the
left, covid data in the middle e.g. 7 day infection rate: 234901 and articles with descriptions 
and links down the right. There should also be two input boxes, three check boxes and a schedule
button at the bottom of the page.  

To remove and replace an article, press the cross in the top right of the displayed article. 20 
articles and loaded with each update and none will appear once you have removed 20 articles, until a schedualed 
update is ran. Click the blue link to go to that articles page and read more. 

To schedule an update:
1. input the time you would like to occur in the first box

2. input a name for the update in the second

3. check whether or not you would like the update to repeate at that time each day

4. check whether or not you would like the data to update

5. check whether or not you would like the news articles to update

6. finaly click submit 

a scheduled update should appear in the top left. click the cross on the update to
cancel and remove the update. 

## Testing
inorder to run the pre programed tests:

1. create a virtual environment called venv by entering "python3 -m venv venv" 
   into the terminal 

2. activate it by entering .\venv\scripts\activate into the terminal

3. enter "setup.py by" into the terminal 

4. enter "pip install e ." 

5. when in venv, enter "pip install -r requirements" into the terminal  

6. then, enter "pytest [module file name]" into the terminal

This will run the tests and output how many tests where passed, and if any didnt pass,
what functions failed their tests. 

## Developer Documentation

## Details 
Author: Lucas Enefer
License: MIT license




