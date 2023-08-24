# spotify-analysis
Trying somethings...


## analysis.py

This Python script allows you to analyze the genres and tracks of a Spotify playlist using the Spotify API. It prompts you to input the ID of the playlist you want to analyze and then provides three options:

View the most listened-to genre or track in the playlist.
View the predominant genre in the playlist.
Extract all genres present in the playlist along with their respective percentages.
The script leverages the Spotipy library to authenticate and interact with the Spotify API. After analyzing the playlist, the results are displayed in the console and saved in a timestamped text file.

>install all dep: 

+ pip install spotipy
+ pip install tqdm

# main.py

This script utilizes the Spotify API to create new playlists based on the genres present in an existing playlist. It prompts you to select a playlist and then proceeds to categorize the tracks by their genres. Subsequently, new playlists are generated for each genre containing the respective tracks. The code uses the Spotipy library for Spotify API interaction and requires user authentication via client credentials. The script facilitates efficient playlist management by automating genre-based track separation.

soon.
