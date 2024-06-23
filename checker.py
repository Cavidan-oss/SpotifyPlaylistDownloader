from fuzzywuzzy import fuzz


class Check(object):

    def __init__(self):
        pass

    def get_token_ratio(self, you_word, spo_word):

        return fuzz.token_set_ratio(you_word, spo_word)

    def get_partial_ratio(self,you_word, spo_word):

        return fuzz.partial_ratio(you_word.lower(), spo_word.lower())



    def check_duration(self,you_dur, spo_dur):
        return True if you_dur-20<spo_dur or you_dur+8<spo_dur else False

    def confirm_indenti(self, spotify_name, youtube_name, spo_dur, you_dur):
        
        return True if self.get_token_ratio(spotify_name, youtube_name) > 75 and self.check_duration(spo_dur, you_dur) else False
