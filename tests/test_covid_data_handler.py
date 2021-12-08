from os import name
from covid_data_handler import parse_csv_data
from covid_data_handler import process_csv_data
from covid_data_handler import covid_api_data_deaths
from covid_data_handler import covid_api_data_hospital_cases
from covid_data_handler import covid_api_request
from covid_data_handler import covid_api_data_new_cases_that_week_nation
from covid_data_handler import covid_api_data_new_cases_that_week_else
from covid_flask_app import seconds




def test_parse_csv_data():
    data = parse_csv_data("nation_2021-10-28.csv")
    assert len(data) == 639, "parse_csv_data: FAILED"

def test_process_csv_data():
    total_deaths , hospital_cases , weeks_cases = process_csv_data(
    parse_csv_data("nation_2021-10-28.csv"))
    assert total_deaths == 141544, "process_csv_data: FAILED"
    assert hospital_cases == 7019,  "process_csv_data: FAILED"
    assert weeks_cases == 240299,   "process_csv_data: FAILED"



def test_covid_api_data_deaths():
    deaths = covid_api_data_deaths([{'cumDeaths28DaysByPublishDate': None},
    {'cumDeaths28DaysByPublishDate':1},{'cumDeaths28DaysByPublishDate':2}])
    assert deaths == "deaths: 1","covid_api_data_deaths: FAILED"

def test_covid_api_data_hospital_cases():
    hospital_cases = covid_api_data_hospital_cases([{'hospitalCases': None},
    {'hospitalCases': 1},{'hospitalCases': 2}])
    assert hospital_cases == "hospital cases: 1", "covid_api_data_hospital_cases: FAILED"

def test_covid_api_data_new_cases_that_week_nation():
    week_cases = covid_api_data_new_cases_that_week_nation(covid_api_request("England","nation"))
    assert week_cases > 0, "covid_api_data_new_cases_that_week_nation: FAILED"
    assert type(week_cases) == int, "covid_api_data_new_cases_that_week_nation: FAILED"

def test_covid_api_data_new_cases_that_week_else():
    week_cases = covid_api_data_new_cases_that_week_else(covid_api_request())
    assert week_cases > 0, "covid_api_data_new_cases_that_week_else: FAILED"
    assert type(week_cases) == int, "covid_api_data_new_cases_that_week_else: FAILED"



if __name__ == "__main__":
    try:
        test_parse_csv_data()
        test_process_csv_data()
        test_covid_api_data_deaths()
        test_covid_api_data_hospital_cases()
        test_covid_api_data_new_cases_that_week_nation()
        test_covid_api_data_new_cases_that_week_else()
    except AssertionError as message:
        print(message)
