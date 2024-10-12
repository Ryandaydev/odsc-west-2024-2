# Running API locally

pip3 install -r requirements.txt

fastapi run main.py

## Tests
pytest test_cruyd.py - tests the crud.py interaction with the database
pytest test_main.py - tests the API code (you don't have to run the API separately, this will run the API during testing)
