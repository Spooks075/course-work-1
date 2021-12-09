from os import name
from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_api_data_deaths
from covid_data_handler import covid_api_data_hospital_cases
from covid_data_handler import covid_API_request
from covid_data_handler import covid_api_data_new_cases_that_week_nation
from covid_data_handler import covid_api_data_new_cases_that_week_else
from covid_data_handler import schedule_covid_updates

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')



def test_parse_csv_data():
    data = parse_csv_data("nation_2021-10-28.csv")
    assert len(data) == 639, "parse_csv_data: FAILED"


def test_covid_api_data_deaths():
    deaths = covid_api_data_deaths({'data':[{'cumDeaths28DaysByPublishDate': None},
    {'cumDeaths28DaysByPublishDate':1},{'cumDeaths28DaysByPublishDate':2}]})
    assert deaths == "deaths: 1","covid_api_data_deaths: FAILED"

def test_covid_api_data_hospital_cases():
    hospital_cases = covid_api_data_hospital_cases({'data':[{'hospitalCases': None},
    {'hospitalCases': 1},{'hospitalCases': 2}]})
    assert hospital_cases == "hospital cases: 1", "covid_api_data_hospital_cases: FAILED"

def test_covid_api_data_new_cases_that_week_nation():
    week_cases = covid_api_data_new_cases_that_week_nation(covid_API_request("England","nation"))
    assert week_cases > 0, "covid_api_data_new_cases_that_week_nation: FAILED"
    assert type(week_cases) == int, "covid_api_data_new_cases_that_week_nation: FAILED"

def test_covid_api_data_new_cases_that_week_else():
    week_cases = covid_api_data_new_cases_that_week_else(covid_API_request())
    assert week_cases > 0, "covid_api_data_new_cases_that_week_else: FAILED"
    assert type(week_cases) == int, "covid_api_data_new_cases_that_week_else: FAILED"



if __name__ == "__main__":
    try:
        test_parse_csv_data()
        test_process_covid_csv_data()
        test_schedule_covid_updates()
        test_covid_API_request()
        test_covid_api_data_deaths()
        test_covid_api_data_hospital_cases()
        test_covid_api_data_new_cases_that_week_nation()
        test_covid_api_data_new_cases_that_week_else()
    except AssertionError as message:
        print(message)
