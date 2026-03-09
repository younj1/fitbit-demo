import requests
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv # python-dotenv module required
import os   # To read environment variable that defines ACCESS_TOKEN

# Read the value of ACCESS_TOKEN from .env file
# Ensure ACCESS_TOKEN is an active token (Generated within 8-hour period)
load_dotenv()
access_token = os.environ['ACCESS_TOKEN']

# headers are included as part of each API call for authentication purposes
# via access token
headers = {'Authorization': f'Bearer {access_token}'}

# Fetches step count data from Fitbit API for a specified date range.
def get_user_steps(day):
    url = f"https://api.fitbit.com/1/user/-/activities/steps/date/{day}/30d.json"
    print(f'URL generated for step data retrieval:\n{url}')
    response = requests.get(url, headers= headers)
    if response.status_code == 200:
        step = response.json()
        step_x_vals = np.array([])
        step_y_vals = np.array([])

        for i in (step["activities-steps"]):
            step_x_vals = np.append(step_x_vals, i["dateTime"])
            step_y_vals = np.append(step_y_vals, i["value"])
            step_y_vals = step_y_vals.astype(int)

            steps_df = pd.DataFrame({'Date': step_x_vals, 'Steps': step_y_vals})
        return steps_df
    else:
        print(f"Error: {response.status_code}")
        return None


# Fetches HRV 5-minute data from Fitbit API for a specified date.
def get_HRV(day):
    url = f"https://api.fitbit.com/1/user/-/hrv/date/{day}/all.json"
    print(f'URL generated for HRV data retrieval:\n{url}')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        HRV_day = response.json()
        hrv_vals = []
        hrv_time = []
        hrv_data = HRV_day['hrv'][0]['minutes']
        # print(hrv_data)
        for data_item in hrv_data:
            hrv_time.append(data_item['minute'])
            hrv_vals.append(data_item['value']['rmssd'])

        df = pd.DataFrame({'time': np.array(hrv_time), 'hrv_rnssd': np.array(hrv_vals)})
        return df

    else:
        print(f"Error: {response.status_code}")
        return None

# Fetches heart rate data per-minute from Fitbit API for a given day.
def get_hr_per_min(day):
    url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{day}/1d/1min.json"
    print(f'URL generated for HR data retrieval:\n{url}')

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        Heart = response.json()
        heart_xvals = np.array([])
        heart_yvals = np.array([])
        heart_xvals = heart_xvals.astype(int)
        for x in (Heart["activities-heart-intraday"]["dataset"]):
            heart_xvals = np.append(heart_xvals, x["time"])
            heart_yvals = np.append(heart_yvals, x["value"])

        df = pd.DataFrame({'time':heart_xvals, 'HR':heart_yvals})
        return df
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    day = input('Enter a date (yyyy-mm-dd): ')
    print()

    df_steps = get_user_steps(day)
    df_steps.to_csv(f'steps-end-{day}.csv')
    print(f'Saving 30-day step data to steps-end-{day}.csv\n\n')

    df_hr = get_hr_per_min(day)
    print(f'Saving heart rate data for {day} to hr-{day}.csv\n\n')
    df_hr.to_csv(f'hr-{day}.csv')

    df_hrv = get_HRV(day)
    print(f'Saving HRV data for {day} to hrv-{day}.csv\n\n')
    df_hrv.to_csv(f'hrv-{day}.csv')

if __name__ == '__main__':
    main()