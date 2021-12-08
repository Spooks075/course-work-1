import json
import sched
import time
import logging
from datetime import datetime
from flask import Flask, render_template
from flask import request
from covid_news_handler import call_articles
from covid_data_handler import call_function

#use code formaters such as black
FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

#gets settings from config file
with open('config.json') as f: 
    config_data = json.load(f)

#global list for api data
data = call_function() 
#global list for api news articals
articles = call_articles() 
#global list for schedualed updates
update_list = [] 



app = Flask(__name__, template_folder='template')
s = sched.scheduler(time.time,time.sleep)

@app.route("/")
def home():
    '''
    
    Description:
    
        Function that renders image, title, covid data, news articles and updates
        as well as checking schedualing 
        
    Arguments:
    
        None
        
    Returns:
    
        render_template {string} : values input into the HTML
        
    '''
    #checks if any schedualed updates are due when the page refreshes
    s.run(blocking=False)

    return render_template('template.html', 
    image = "catimage.jpg", 
    title = "covid data and news board", 
    location = config_data["local location"],
    nation_location = config_data["nation location"],
    local_7day_infections = data[0], 
    national_7day_infections = data[1], 
    hospital_cases =  data[2],
    deaths_total =  data[3], 
    news_articles = articles[0:4], 
    updates = update_list 
    )

def update_function(up_news:str,up_data:str) -> str: 
    '''
    
    Description:
    
        Function that updates covid data and news and checks if update 
        should be scheduled again or not
        
    Arguments:
    
        up_news {string} : states whether or not to update data
        up_data {string} : states whether or not to update news
        
    Returns:
    
        home {function} : runs home function
        
    '''
    logging.info('SCHEDULED UPDATE RAN')

    global data 
    global articles 
    if up_data == 'true': 
        logging.info('COVID DATA UPDATED')
        data = call_function() 
    if up_news == 'true':
        logging.info('COVID ARTICLES UPDATED')
        articles = call_articles() 

    #goes through each item in update list
    for item in update_list: 
        if (item['sched update'] not in s.queue) and (item['repeat'] == 'true'): 
            #if update has been run and is supposed to repeat
            sched_update = s.enter(seconds(item['input time']),
            1,update_function,(item['covid data'],item['covid news']))
            item['sched update'] = sched_update 
            logging.info('UPDATE RE SCHEDULED')
        elif (item['sched update'] not in s.queue) and (item['repeat'] == 'false'): 
            #if update has been run but is not supposed to repeat
            update_list.remove(item) 
            logging.info('UPDATE REMOVED FROM LIST')

    return home() 


def seconds(input_time:str) -> int: 
    '''
    
    Description:
    
        Function that calculates the number of seconds till schedualed
        update should run
        
    Arguments:
    
        input_time {string} : the input time of when the update should run
        
    Returns:
    
        time_till {int} : number of seconds unti update should run
        
    '''
    #and returns seconds until that time
    now = datetime.now() 
    hour = int(now.strftime("%H")) 
    minute = int(now.strftime("%M")) 
    second = int(now.strftime("%S")) 
    #takes current hour away from input hour
    hour = int(input_time[0:2]) - hour 
    #takes current minute away from input
    minute = int(input_time[3:]) - minute 
    #if minute is less than 0 then update is tomorrow 
    if minute < 0:  
        minute += 60 
        hour += 24 
    #if hour less than 0 then update is for tomorrow so
    elif hour < 0: 
        hour += 24 
    #if seconds till update is 0 then update is the same time tommorow so
    if (((hour*60)+minute)*60) == 0: 
        hour += 24 
    #coverts hours and minutes into seconds 
    time_till = (((hour*60)+minute)*60)+second 
    logging.info('TIME TILL UPDATE CALCULATED')
    return time_till

@app.route("/index",methods = ["GET"])
def close_button() -> str:
    '''
    
    Description:
    
        Function that runs when a cross button is pressed that removes updates 
        and news articles when their cross is clicked as well as creating and update
        and adding it to the update list when create update is pressed
        
    Arguments:
    
        None
        
    Returns:
    
        home {function} : runs home function'''

    s.run(blocking=False)

    #when cross is pressed on articles
    if request.args.get("notif"): 
        #gets the title of article that thr cross was clicked
        title = request.args.get("notif") 
        for news in articles:
            #goes through articals till title matches then removes that article from list
            if news['title'] == title:  
                articles.remove(news)
                logging.info('ARTICLE ')
 
    #when the update button is pressed
    if request.args.get('update'): 
        input_time = request.args.get('update')
        name = request.args.get('two')

       
        #converts toggle buttons to true or false strings
        if request.args.get('repeat') is not None: 
            repeat = 'true'
        else:
            repeat = 'false'
        if request.args.get('covid-data') is not None:
            covid_data = 'true'
        else:
            covid_data = 'false'
        if request.args.get('news') is not None:
            covid_news = 'true' 
        else:
            covid_news = 'false'

        #schedules an update with input specifications
        sched_update = s.enter(seconds(input_time),1,update_function,(covid_data, covid_news))  
        
        #creates dictionary with updates specifications
        update_dict = {'title':'name: '+name,  
        'content':'time: '+input_time
        +' updating covid data: '+str(covid_data)
        +' updating covid news: '+str(covid_news)
        +' repeating: '+str(repeat),
        'repeat' : repeat,
        'input time': input_time,
        'covid data': covid_data,
        'covid news':covid_news,
        'sched update' : sched_update
        }
        #adds dictionary to list of updates
        update_list.append(update_dict)

        logging.info('UPDATE SCHEDULED')
        

    #if update cross is clicked
    if request.args.get('update_item'): 
        #gets title of update cross clicked
        title = request.args.get("update_item") 
        for items in update_list:
            #gets title of update cross clicked
            if items['title'] == title:
                update_list.remove(items)
                for updates in s.queue:
                    #finds update in scheduled updated and cancels it
                    if updates[4] == items['title']: 
                        s.cancel(updates)
                        logging.info('UPDATED CANCELED')

    
    return home()

if __name__ == "__main__":
    app.run(debug=True)