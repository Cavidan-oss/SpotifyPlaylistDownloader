import base64
import requests
import datetime
from urllib.parse import urlencode





class SpotifyApi(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    data = None
    music_id = None
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):

        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        """
        Update the access token and expiration date
        """

        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)

        if r.status_code not in range(200, 299):
            return False

        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_playlist_items(self, playlist_id, **kwargs):
        """
        Loads the all items details
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = urlencode(kwargs)
        total_url = f"{url}?{data}"
        response = requests.get(total_url, headers = headers)

        if response.status_code not in range(200,299):
            return {}


        self.data = response.json()

        return response.json()

    def parse_playlist(self, playlist_id):
        data = self.get_playlist_items(playlist_id)
        self.music_id = {}
        for value in data['items']:
            self.music_id[value['track']['id']] = [f"{'&'.join([value['name'] for index,value in enumerate(value['track']['artists']) if index<2])} : {value['track']['name']}",value['track']['duration_ms']//1000] 
            

        return self.music_id

    def get_musics_name(self):

        return {index : musics[0] for index,musics in self.music_id.items()}
    
    def get_musics_length(self):

        return {index:musics[1] for index, musics in self.music_id.items()}    





