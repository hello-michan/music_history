from flask import Flask, render_template, request
import pandas as pd
import os
import glob

###################################################################################
###################################################################################
# analyse Most 5 Played Artists & Songs
###################################################################################
###################################################################################
app = Flask(__name__)

def load_spotify_data():
    # Path to data folders
    folder_path = "data"

    #Get files from the folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))

    #intialise the list
    df_file = []
    #read each files
    for file in json_files:
        df_file.append(pd.read_json(file))
    
    df = pd.concat(df_file, ignore_index=True)

    # convert milliseconds to hour
    df["hoursPlayed"] = df["msPlayed"] / (1000*60*60)

    # convert endTime to year-month 
    df["ts"] = pd.to_datetime(df["endTime"])
    df["month"] = df["ts"].dt.strftime('%Y-%m')

    return df

spotify_df = load_spotify_data()


@app.route("/",methods=["GET", "POST"])
def index():
    # Get the top 5 artists
    top_artists = (
        spotify_df.groupby("artistName")["hoursPlayed"]
        .sum()
        .reset_index()
        .sort_values(by="hoursPlayed", ascending=False)
        .head(5)
    )
    # Get the top 5 songs
    top_songs = (
        spotify_df.groupby(["trackName","artistName"])["hoursPlayed"]
        .sum()
        .reset_index()
        .sort_values(by="hoursPlayed", ascending=False)
        .head(5)
    )
    # Get the options
    all_months = spotify_df["month"].unique()

    # instantiate selected month 
    selected_month = None  
    # instantiate 
    top_artists_monthly = []

    if request.method == "POST":
        selected_month = request.form.get("dropdown")
        if selected_month:
            # Get top 3 artists based on the selected month
            top_artists_monthly = (
                spotify_df[spotify_df["month"] == selected_month]
                .groupby("artistName")["hoursPlayed"]
                .sum()
                .reset_index()
                .sort_values(by="hoursPlayed", ascending=False)
                .head(3)
            ).to_dict(orient="records") 


    return render_template(
        "index.html",
        top_artists=top_artists,
        top_songs=top_songs, 
        top_artists_monthly=top_artists_monthly, 
        months=all_months,
        selected_month=selected_month)


if __name__ == "__main__":
    app.run(debug=True)