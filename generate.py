import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm  # Para a barra de progresso
import datetime

# Configurações de autenticação
SPOTIPY_CLIENT_ID = 'client_id'
SPOTIPY_CLIENT_SECRET = 'secret_id'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'  # URL de redirecionamento

# Inicialização da API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-library-read playlist-modify-public'))

def create_genre_playlists(playlist_id):
    try:
        # Obtém informações da playlist
        playlist = sp.playlist(playlist_id)
        tracks = playlist['tracks']['items']

        # Dicionário para mapear gêneros musicais às faixas
        genre_tracks = {}

        # Classifica as faixas por gênero
        for track in tqdm(tracks, desc="Classificando faixas"):
            track_info = track['track']
            track_id = track_info['id']
            track_features = sp.audio_features(track_id)[0]
            
            artists = track_info['artists']
            track_artist_ids = [artist['id'] for artist in artists]
            track_artist_info = sp.artists(track_artist_ids)
            track_genres = []
            for artist_info in track_artist_info['artists']:
                genres = artist_info.get('genres', [])
                track_genres.extend(genres)
            
            for genre in track_genres:
                if genre not in genre_tracks:
                    genre_tracks[genre] = set()  # Usar um conjunto para evitar duplicatas
                genre_tracks[genre].add(track_id)

        genre_choices = list(enumerate(genre_tracks.keys(), start=1))

        if not genre_choices:
            print("Nenhum gênero encontrado nas faixas da playlist.")
            return

        print("Gêneros disponíveis:")
        for num, genre in genre_choices:
            track_count = len(genre_tracks[genre])
            print(f"{num}: {genre} ({track_count} músicas)")

        selected_genre_numbers = input("Insira os números dos gêneros que deseja criar playlists (separados por vírgula): ")
        selected_genre_numbers = [int(num) for num in selected_genre_numbers.split(',')]

        selected_genres = [genre for num, genre in genre_choices if num in selected_genre_numbers]

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"playlist_generation_logs_{timestamp}.txt"
        result_text = ""

        for genre in selected_genres:
            playlist_name = input(f"Insira o nome da playlist para o gênero '{genre}': ")
            new_playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=True)
            sp.playlist_add_items(playlist_id=new_playlist['id'], items=list(genre_tracks[genre]))  # Convertendo conjunto para lista
            result_text += f"Playlist '{playlist_name}' criada para o gênero '{genre}' com {len(genre_tracks[genre])} músicas.\n"

        save_results_to_file(filename, result_text)
        print("Playlists criadas com sucesso! Logs salvos em:", filename)
    except Exception as e:
        print(f"Falha ao criar playlists: {e}")

def save_results_to_file(filename, result_text):
    with open(filename, "w") as file:
        file.write(result_text)

if __name__ == "__main__":
    playlist_id = input("Insira o ID da playlist que deseja separar por gênero: ")
    create_genre_playlists(playlist_id)
