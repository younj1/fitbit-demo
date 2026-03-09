import requests
import pandas as pd
import numpy as np
#imported json 
import json
from datetime import datetime
from dotenv import load_dotenv 
import os  

load_dotenv()
access_token = os.environ['ACCESS_TOKEN']


headers = {'Authorization': f'Bearer {access_token}'}

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


def get_HRV(day):
    url = f"https://api.fitbit.com/1/user/-/hrv/date/{day}/all.json"
    print(f'URL generated for HRV data retrieval:\n{url}')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        HRV_day = response.json()
        hrv_vals = []
        hrv_time = []
        if HRV_day['hrv']:
            print(HRV_day)
            hrv_data = HRV_day['hrv'][0]['minutes']
            
            for data_item in hrv_data:
                hrv_time.append(data_item['minute'])
                hrv_vals.append(data_item['value']['rmssd'])

            df = pd.DataFrame({'time': np.array(hrv_time), 'hrv_rnssd': np.array(hrv_vals)})
            return df
        else:
            
            df = pd.DataFrame()
            return df

    else:
        print(f"Error: {response.status_code}")
        return None


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


def get_user_zone(day):
    url = f"https://api.fitbit.com/1/user/-/activities/active-zone-minutes/date/{day}/30d.json"
    print(f'URL generated for Zone data retrieval:\n{url}')

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        zone = response.json()

        # Print the raw JSON object to the terminal
        print("\nRaw JSON response for active zone minutes:")
        print(json.dumps(zone, indent=3))

        # Lists to hold each column of data extracted from the JSON
        dates = []
        fat_burn_mins = []
        cardio_mins = []
        peak_mins = []
        total_azm = []

        # Each entry in the list contains a date and a nested value dict with zone breakdowns
        for entry in zone["activities-active-zone-minutes"]:
            dates.append(entry["dateTime"])
            val = entry["value"]
            # Some days may not have every zone key; default to 0 if missing
            fat_burn_mins.append(val.get("fatBurnActiveZoneMinutes", 0))
            cardio_mins.append(val.get("cardioActiveZoneMinutes", 0))
            peak_mins.append(val.get("peakActiveZoneMinutes", 0))
            total_azm.append(val.get("activeZoneMinutes", 0))

        # Build a DataFrame with one row per day
        zone_df = pd.DataFrame({
            'Date': dates,
            'Fat Burn Zone (min)': fat_burn_mins,
            'Cardio Zone (min)': cardio_mins,
            'Peak Zone (min)': peak_mins,
            'Total Active Zone Minutes': total_azm
        })

        # Save the DataFrame to a CSV file named with the ending date
        csv_filename = f'zone-end-{day}.csv'
        zone_df.to_csv(csv_filename, index=False)
        print(f'\nSaving 30-day active zone minutes data to {csv_filename}\n')

        return zone_df
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

    # Fetch and save active zone minutes for the 30 days ending on the entered date
    get_user_zone(day)

if __name__ == '__main__':
    main()