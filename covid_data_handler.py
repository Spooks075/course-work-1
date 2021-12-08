'''

Description:

    module gets covid data from and api and a csv file
    it then finds and calculates the number of deaths,
    number of hospital cases and the 7 day infection rate

'''


import json
from uk_covid19 import Cov19API


#gets settings from config file
with open('config.json', encoding="utf-8") as f:
    config_data = json.load(f)

#filter for API request
cases_and_deaths = {

        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate":"newCasesBySpecimenDate"
    }

def parse_csv_data(csv_filename:str = "nation_2021-10-28.csv") -> list:
    '''

    Description:

        Function that gets covid data from csv file

    Arguments:

        csv_filename {string} : a string containing the file name for the csv file

    Returns:

        csv_data {list} : a list containg the csv covid data

    '''
    csv_data = []
    #reads all the lines in the file into a list and remouves the new line symbol
    csv_data = open(csv_filename , 'r').readlines()
    return csv_data

def process_csv_data(covid_csv_data:list) -> tuple[int,int,int]:
    '''

    Description:

        Function that gets the number of deaths, number of hospital cases and 7 day infection rate
        from covid csv data

    Arguments:

        covid_csv_data {list} : a list containg the csv covid data

    Returns:

        deaths {int} : the number of deaths
        hospital_cases {int} : the number of hospital cases
        weeks_cases {int} : the 7 day infection rate

    '''
    deaths = 0
    hospital_cases = 0
    weeks_cases = 0
    count = 0
    #goes through each line in the csv data
    for line in covid_csv_data:
        line = line.strip().split(',')
        #finds first instance of deaths in which its value is neither the title or null
        if line[4] != '' and deaths == 0 and line[4] != 'cumDailyNsoDeathsByDeathDate':
            deaths = int(line[4])
        #finds first instance of hospital cases in which its value is neither the title or null
        if line[5] != '' and hospital_cases == 0 and line[5] != 'hospitalCases':
            hospital_cases = int(line[5])
        #finds first instance of cases in which its value is neither the title or null
        if line[6] != '' and count == 0 and line[6] != 'newCasesBySpecimenDate':
            count = 1 #skips the first days value
        # iterates through the next 7 days and sums the values
        elif count > 0 and count < 8:
            weeks_cases += int(line[6])
            count += 1

    return deaths, hospital_cases, weeks_cases


def covid_api_request(location:str = 'Exeter', location_type:str = 'ltla') -> list:
    '''
    Description:

        Function which gets the covid data from the api

    Arguments:

        location {string} : the name of the location to get the api covid data for
        location_type {string} : the type of location to get the covid api data for

    Returns:

        new_data {list} : a list of dictionarys containing 4 sub dictionary's:
                      {newCasesByPublishDate} {cumDeaths28DaysByPublishDate}
                      {hospitalCases} {newCasesBySpecimenDate}
    '''

    default_filters = [
        'areaType='+location_type,
        'areaName='+location
    ]
    #creates the API request
    api = Cov19API(filters=default_filters,structure=cases_and_deaths)
    #requests the API data
    data = api.get_json()
    #filters down to a list of just a list of the dictionarys for the data of each day
    new_data = data['data']
    return new_data


def covid_api_data_deaths(data:list) -> str:
    '''

    Description:

        Function which gets total number of covid deaths from the covid api data

    Arguments:

        data {list} : a list of dictionarys containing 4 sub dictionary's:
                      {newCasesByPublishDate} {cumDeaths28DaysByPublishDate}
                      {hospitalCases} {newCasesBySpecimenDate}

    Returns:

        deaths {string} : a string contaning the number of deaths

    '''
    count=0
    #gets the data for today
    that_days_data = data[count]

    #goes through each days hospital cases data until that data does not equal none
    while that_days_data['cumDeaths28DaysByPublishDate'] is None:
        count += 1
        that_days_data = data[count]
    deaths = "deaths: " + str(that_days_data['cumDeaths28DaysByPublishDate'])
    return deaths

def covid_api_data_hospital_cases(data:list) -> str:
    '''

    Description:

        Function which gets the current number of hospital cases from the covid api data

    Arguments:

        data {list} : a list of dictionarys containing 4 sub dictionary's:
                      {newCasesByPublishDate} {cumDeaths28DaysByPublishDate}
                      {hospitalCases} {newCasesBySpecimenDate}

    Returns:

        hospital_cases {string} : a string containing the number of current hospital cases

    '''
    count = 0
    #gets the data for the today
    that_days_data = data[count]
    #goes through each days hospital cases data until that data does not equal none
    while that_days_data['hospitalCases'] is None:
        count += 1
        that_days_data = data[count]
    #adds that days hospital cases to a string and then returns it
    hospital_cases = "hospital cases: " + str(that_days_data['hospitalCases'])
    return hospital_cases

def covid_api_data_new_cases_that_week_nation(data:list) -> int:
    '''

    Description:

        Function which gets the 7 day infection rate for the
        specified nation from the covid api data

    Arguments:

        data {list} : a list of dictionarys containing 4 sub dictionary's:
                      {newCasesByPublishDate} {cumDeaths28DaysByPublishDate}
                      {hospitalCases} {newCasesBySpecimenDate}

    Returns:

        new_cases_that_week {intger} : an intiger with the 7 day infection rate for that nation

    '''
    new_cases_that_week = 0
    count_1 = 0
    #gets the data for that day
    that_days_data = data[count_1]
    #goes through each days cases until it does not equal none
    while that_days_data['newCasesByPublishDate'] is None:
        count_1 += 1
        that_days_data = data[count_1]
    count_2 = 0
    #then goes through the next 7 days
    while count_2 != 7:
        that_days_data = data[count_1]
        #adds those days cases together
        new_cases_that_week += that_days_data['newCasesByPublishDate']
        count_1 += 1
        count_2 +=1
    return new_cases_that_week


def covid_api_data_new_cases_that_week_else(data:list) -> int:
    '''

    Description:

        Function which gets the 7 day infection rate for the
        specified local area from the covid api data

    Arguments:

        data {list} : a list of dictionarys containing 4 sub dictionary's:
                      {newCasesByPublishDate} {cumDeaths28DaysByPublishDate}
                      {hospitalCases} {newCasesBySpecimenDate}

    Returns:

        new_cases_that_week {intger} : an intiger with the 7 day infection rate for that local area

    '''
    new_cases_that_week = 0
    count_1 = 0
    #gets the data for that day
    that_days_data = data[count_1]
    #goes through each days cases until it does not equal none
    while that_days_data['newCasesBySpecimenDate'] is None:
        count_1 += 1
        that_days_data = data[count_1]

    count_2 = 0
    #then goes through the next 7 days
    while count_2 != 7:
        that_days_data = data[count_1]
        #adds those days cases together
        new_cases_that_week += that_days_data['newCasesBySpecimenDate']
        count_1 += 1
        count_2 += 1
    return new_cases_that_week

def call_function() -> list:
    '''

    Description:

        Funuction used to pass covid api data into flask

    Arguments:

        none

    Returns:

        data {list} : a list of covid api data:
        local 7 day infection rate, national 7 day infection rate,
        national hospital cases, national deaths

    '''
    data = [covid_api_data_new_cases_that_week_nation(
        covid_api_request(config_data["local location"],)),
    covid_api_data_new_cases_that_week_else(
        covid_api_request(config_data["nation location"],'nation')),
    covid_api_data_hospital_cases(
        covid_api_request(config_data["nation location"],'nation')),
    covid_api_data_deaths(
        covid_api_request(config_data["nation location"],'nation'))]
    return data
