import re
from file_handler import File_Handler
from music_downloader import YoutubeDownloader
from checker import Check
from music_finder import SpotifyApi
import os 
from itertools import islice
from datetime import datetime as dt
from time import sleep
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urlencode





class Main(SpotifyApi, File_Handler):
	musics_name = None

	def __init__(self, client_id, client_secret, *args, **kwargs):
		super().__init__(client_id, client_secret)
		self.client_id = client_id
		self.client_secret = client_secret
		self.check =  Check()

		self.perform_auth()


	def download_playlist(self, spofy_list_url):
		"""
		Downloads the whole playlist
		"""

		self.data = self.parse_playlist(spofy_list_url)
		self.create_path()
		data = []

		for id, info in self.data.items():

			self.musics_name, self.music_duration= info[0].replace(':','-'), info[1]
			#query = "+".join(self.musics_name.split(' ')).encode(encoding = 'UTF-8', errors = 'strict')
			#search_query = f"https://www.youtube.com/results?search_query={query}"


			base = f"https://www.youtube.com/results"
			query = "".join(self.musics_name.split(' ')).encode(encoding = 'UTF-8', errors = 'strict')
			search_query = f"{base}?{urlencode({'search_query':query})}"

			links = self.get_video_links(search_query)
			
			if links:
				for link in links:

					downloader = YoutubeDownloader(link)
					l_music_name = downloader.get_video_title()
					l_duration = downloader.get_video_duration()

					if self.check.confirm_indenti(self.musics_name, l_music_name, self.music_duration, l_duration):
						try:
							downloader.download_as_music()

							
						except:
							print(f'Download Error for :{self.musics_name}')
							print(f'{self.musics_name} | Problem - {Exception}')
						else:			
							print(f'{self.musics_name} Downloaded_name {l_music_name} |Sucess')
						
						break
						
			else:
				print(f"{self.musics_name} Not links found{links}")

		return data

	def create_path(self, folder_name = None):
		"""
		Creates and Changes directory to the specified
		"""

		if not folder_name:
			now = dt.now()
			folder_name = now.strftime("%B_%d(%Y)")

		self.change_dir_to('downloads')

		if not os.path.exists(os.path.join(os.getcwd(), folder_name)):
			self.create_folder(folder_name)

		self.change_dir_to(folder_name)


	def get_video_links(self,search_url, limit = 6):
		"""
		Returns the youtube links in a specified limit
		"""
		
		#html = urllib.request.urlopen(search_url)
		#sleep(1)
		soup = self.get_soup(search_url)

		#video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
		video_ids = re.findall(r"watch\?v=(\S{11})", str(soup))


		return [f"https://www.youtube.com/watch?v={id}" for id in video_ids[:limit]]


	def get_soup(self, url):
    
	    while True:
	    	try:
	            request=requests.get(url)
	        	break
	        
	        except:
	            print("Error Occured. Reconnecting!!!!")
	    
	    content=request.content

	    soup=BeautifulSoup(content, 'html.parser')
	    
	    return soup





load_dotenv()
client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")

music = Main(client_id, client_secret)


print(music.download_playlist('37i9dQZEVXbIVYVBNw9D5K'))


