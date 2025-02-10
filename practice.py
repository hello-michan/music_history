import pandas as pd
import os
import glob

###################################################################################
###################################################################################
# analyse the Most 5 Played Artists per month
###################################################################################
###################################################################################

# Path to the folder containing json files
folder_path = "data"

# Get all json file paths
json_files = glob.glob(os.path.join(folder_path, "*.json"))

# Initialise an empty list 
df_list = []

# Loop through each json file and read it
for file in json_files:
    df = pd.read_json(file)
    df_list.append(df)

# Combine all of teh data into one file
df_combined = pd.concat(df_list, ignore_index=True)


# convert msPlayed to minutes
df_combined["hourPlayed"] = df_combined["msPlayed"] / (1000 * 60 * 60)

#convert end time to time stampt 
df_combined['ts'] = pd.to_datetime(df_combined['endTime'])
df_combined['monthly'] = df_combined['ts'].dt.strftime('%Y-%m')

# group by artists and sum up the playtime
top_artists_per_month = df_combined.groupby(
    ['monthly', 'artistName'])["hourPlayed"].sum().reset_index()

# Sort by the month
top_5_artists_monthly = top_artists_per_month.sort_values(["monthly","hourPlayed"], ascending=[True,False]).groupby('monthly').head(2)

print(top_5_artists_monthly[["monthly", "artistName","hourPlayed"]])

# select month
