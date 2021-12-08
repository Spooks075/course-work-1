from covid_flask_app import seconds

def test_seconds():
    time = seconds("12:00")
    assert type(time) == int, "seconds: FAILED"
    assert time > 0,    "seconds: FAILED"



if __name__ == "__main__":
    try:
        test_seconds()
    except AssertionError as message:
        print(message)