import requests
import pandas as pd
import numpy as np

from dotenv import load_dotenv # python-dotenv module required
import os   # To read environment variable that defines ACCESS_TOKEN

# Read the value of ACCESS_TOKEN from .env file
# Ensure ACCESS_TOKEN is an active token (Generated within 8-hour period)
load_dotenv()
access_token = os.environ['ACCESS_TOKEN']

# Headers for the API request
headers = {
    'Authorization': f'Bearer {access_token}'
}

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
