import pafy
from datetime import datetime as dt


class YoutubeDownloader(object):

  url = ''

  def __init__(self, url):
    self.url = url
    self.video = pafy.new(url)
  
  def setup(self, url):
    self.video = pafy.new(url)

  def download_as_music(self):
      url = self.url
      self.music = self.video.audiostreams
      index = self.get_needed_form('m')
      
      self.music[index].download()

  def get_needed_form(self, mode = 'v'):

      for index, value in enumerate(self.music):
        if value.extension == 'm4a' and mode == 'm':
          
          return index
        
      return index

  def get_video_title(self):

      return self.video.title

  def get_video_duration(self):
      
      return self.convert_second(self.video.duration)


  def download_as_video(self, quality = 3):
      
      url = self.url
      self.video =  self.video

  def convert_second(self, time):
      date_time = dt.strptime(time, "%H:%M:%S")
      timedelta = date_time - dt(1900, 1, 1)
      seconds = timedelta.total_seconds()

      return int(seconds)


  def get_video_id(self):

    return self.video.videoid


  def get_view_count(self):

    return  self.video.viewcount
