import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from tqdm import tqdm
import datetime

# Configurações de autenticação
SPOTIPY_CLIENT_ID = 'client_id'
SPOTIPY_CLIENT_SECRET = 'client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'  # URL de redirecionamento

# Inicialização da API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-library-read playlist-read-private'))

def extract_genres_from_playlist(playlist_id):
    playlist = sp.playlist(playlist_id)
    tracks = playlist['tracks']['items']
    
    all_artist_genres = []
    all_track_names = []
    
    for track in tqdm(tracks, desc="Extraindo informações"):
        track_info = track['track']
        artists = track_info['artists']
        track_artists = [artist['name'] for artist in artists]
        
        for artist in track_artists:
            artist_info = sp.search(q=artist, type='artist', limit=1)
            if artist_info and 'artists' in artist_info and 'items' in artist_info['artists']:
                genres = artist_info['artists']['items'][0].get('genres', [])
                all_artist_genres.extend(genres)
        
        all_track_names.append(track_info['name'])

    return all_artist_genres, all_track_names

def save_results_to_file(filename, result_text):
    with open(filename, "w") as file:
        file.write(result_text)

def main():
    playlist_id = input("Insira o ID da playlist que deseja analisar: ")
    genres, track_names = extract_genres_from_playlist(playlist_id)
    
    print("Opções:")
    print("1. Ver gênero/música mais escutada da playlist")
    print("2. Ver gênero mais predominante da playlist")
    print("3. Extrair todos os gêneros da playlist e suas porcentagens")
    
    choice = input("Escolha uma opção (1, 2 ou 3): ")
    
    result_text = ""

    if choice == "1":
        most_listened_track_name = Counter(track_names).most_common(1)[0][0]
        result_text = f"Gênero/música mais escutada: {most_listened_track_name}"
    
    elif choice == "2":
        genre_counts = Counter(genres)
        total_count = len(genres)
        most_common_genre = genre_counts.most_common(1)
        most_common_genre_name = most_common_genre[0][0]
        most_common_genre_percentage = (most_common_genre[0][1] / total_count) * 100
        result_text = f"Gênero mais predominante: {most_common_genre_name} ({most_common_genre_percentage:.2f}%)"
    
    elif choice == "3":
        genre_counts = Counter(genres)
        total_count = len(genres)
        result_text = "Gêneros presentes na playlist e suas porcentagens:\n"
        for genre, count in genre_counts.items():
            percentage = (count / total_count) * 100
            result_text += f"{genre}: {percentage:.2f}%\n"
    
    else:
        print("Opção inválida.")
        return

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"playlist_analysis_{timestamp}.txt"
    save_results_to_file(filename, result_text)
    print(f"Resultados salvos no arquivo: {filename}")

if __name__ == "__main__":
    main()
