# Wildfire Hex Plot

### View
https://bdbi-wildfire-vis.herokuapp.com/

### Run with pip
Navigate to the project root
> pip install -r requirements.txt
> 
> python app.py

Open http://127.0.0.1:8050/ 


### Run with pipenv
> pipenv install
> 
> pipenv run python app.py

Open http://127.0.0.1:8050/ 


### Contributing

#### Tests
Tests must go into the tests folder

Test files must be of form:
> test_X.py


#### Linting
This uses flake8 for linting

In VSCode, do ctrl + shift + p, search for enable linter and select linter, and install flake8

The linter will check files on save

#### CI / CD
CI is through Github Actions

CD is not set up, but deployment is through Heroku