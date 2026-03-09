import fitbit
import requests
import pandas as pd
import numpy as np

from dotenv import load_dotenv, set_key
import os

load_dotenv()
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']

def save_tokens(token):
    set_key('.env', 'ACCESS_TOKEN', token['access_token'])
    set_key('.env', 'REFRESH_TOKEN', token['refresh_token'])

auth_client = fitbit.Fitbit(
    CLIENT_ID, CLIENT_SECRET,
    oauth2=True,
    access_token=ACCESS_TOKEN,
    refresh_token=REFRESH_TOKEN,
    refresh_cb=save_tokens
)

# Fetches step count data from Fitbit API for a specified date range.
def get_user_steps(ending_day):
    url = f"https://api.fitbit.com/1/user/-/activities/steps/date/{ending_day}/1w.json"
    response = requests.get(url, headers= headers)
    if response.status_code == 200:
        step = response.json()
        step_x_vals = np.array([])
        step_y_vals = np.array([])

        for i in (step["activities-steps"]):
            step_x_vals = np.append(step_x_vals, i["dateTime"])
            step_y_vals = np.append(step_y_vals, i["value"])
            step_y_vals = step_y_vals.astype(int)

            steps_df = pd.DataFrame({'Day': step_x_vals, 'Steps': step_y_vals})
        return steps_df

    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    ending_day = input('Enter ending day (yyyy-mm-dd): ')
    df = get_user_steps(ending_day)
    print(df)

if __name__ == '__main__':
    main()
