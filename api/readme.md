# Running API locally

    pip3 install -r requirements.txt
    fastapi run main.py

## Tests

Test the crud.py interaction with the database:
    
    pytest test_crud.py 

Test the API code (you don't have to run the API separately, this will run the API during testing):
    
    pytest test_main.py 
