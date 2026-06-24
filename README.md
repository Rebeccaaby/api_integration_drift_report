# Weather Drift Report

A configuration-driven Python application that retrieves weather data from two different wehater providers for the same locations, normalizes the responses, compares them, and generates a drift report highlighting differences between sources.

# 1. Setup Instructions

## Prerequisites:
- Python 3.8 or higher
- A free WeatherAPI.com account and API key
- A free RapidAPI account subscribed to the Meteostat free plan

### Step 1 - Clone the Repository
`git clone https://github.com/Rebeccaaby/api_integration_drift_report.git` \
`cd api_integration_drift_report`

### Step 2 — Create a Virtual Environment
`python -m venv venv`

#### Windows
- `venv\Scripts\activate`

#### Mac/Linux
- `source venv/bin/activate`

### Step 3 - Install Dependencies
- `pip install -r requirements.txt`

### Step 4 — Create Your Secrets File

The file `src/config/secrets.yaml` is not included in this repository for not including api keys.
Create it manually:
- In VS Code, navigate to src/config/ and create a new file called secrets.yaml. A template is provided in secrets.yaml.example. Add your keys in this exact format below.
- api_keys: \
    &emsp;weatherapi: "YOUR_WEATHERAPI_KEY_HERE"\
    &emsp;meteostat: "YOUR_METEOSTAT_RAPIDAPI_KEY_HERE"

#### Where to get your keys:

WeatherAPI: sign up at weatherapi.com -> Dashboard -> copy API Key
Meteostat: sign up at rapidapi.com -> subscribe to free plan -> copy x-rapidapi-key

### Step 5 — Add a New Location (Optional)

- Open src/config/settings.yaml and add a new entry under locations. No code changes are required

## How to Run

Make sure your virtual environment is active(Step 2) and you are in the project root folder where main.py lives, then run:
- `python main.py`

### Output
After a successful run there is a console report printed to the terminal and two files saved automatically under:
- reports/ \
  &emsp;drift_report.json \
  &emsp;drift_report.csv

- A sample of real output is already included in the reports/ folder so results can be reviewed without running the application or obtaining API keys.

## Expected Console Output

![alt text](image.png)