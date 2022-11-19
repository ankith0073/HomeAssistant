import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

saturday = 5
sunday = 6

playlist_hans_zimmer = "https://open.spotify.com/playlist/37i9dQZF1DWWF3yivn1m3D?si=788d257f971c45de"
playlist_evening_chill = "https://open.spotify.com/playlist/6iKXlATWH4MPtahYaLCeMn?si=532436c972db4c4e"
playlist_jazz_vibes = "https://open.spotify.com/playlist/37i9dQZF1DX0SM0LYsmbMT"
playlist_kannada = "https://open.spotify.com/playlist/4nRDM69vmrfaqCKqi1aQmc"
playlist_rainy_day = "https://open.spotify.com/playlist/37i9dQZF1DXbvABJXBIyiY"
playlist_chil_vibes = "https://open.spotify.com/playlist/37i9dQZF1DX889U0CL85jj"
playlist_sunny_day = "https://open.spotify.com/playlist/37i9dQZF1DX1BzILRveYHb"
playlist_cloudy_day = "https://open.spotify.com/playlist/37i9dQZF1DX6lttj7ulLd6"
playlist_winter = "https://open.spotify.com/playlist/37i9dQZF1DX4je779Ww5L2"
playlist_snow = "https://open.spotify.com/playlist/37i9dQZF1DZ06evO3bXBF7"
playlist_grand_sounds = "https://open.spotify.com/playlist/4o7ysYl3CaIPlDt4UKclRU"

weekend_playlist = "https://open.spotify.com/playlist/37i9dQZF1DX2hL79MX8oXQ"


class Music(hass.Hass):
    def initialize(self):
        runtime = datetime.time(17, 30, 0)
        self.run_daily(self.TurnOnEveningMusiccb, runtime)
        
        runtime = datetime.time(21, 00, 0)
        self.run_daily(self.TurnOnEveningLightcb, runtime)
        
        runtime = datetime.time(23, 00, 0)
        self.run_daily(self.StopMusic, runtime)
        
        tv_name = "media_player.sonos_living_room"
        self.tv_enitity = self.get_entity(tv_name)
        
        #=====Weekend Music========================#
        runtime = datetime.time(8, 00, 00)
        handle = self.run_daily(self.WeekendMusicOn, runtime)
    
    def TurnOnEveningMusiccb(self, kwargs):
        listUrl = self.getplaylist()
        self.log("Current chosen playlist %s", listUrl)
        if self.trigger_event():
            self.PlayMusic(listUrl)
    
    def TurnOnEveningLightcb(self, kwargs):
        listUrl = playlist_jazz_vibes
        if self.trigger_event():
            self.PlayMusic(listUrl)
            
    def WeekendMusicOn(self, kwargs):
        listUrl = self.getplaylist()
        self.log("Current chosen playlist %s", listUrl)
        if self.trigger_event():
            if datetime.datetime.today().weekday() in [saturday,sunday]:
              self.PlayMusic(listUrl)
        
    def PlayMusic(self, playListURL = ''):
        try:
            self.my_enitity = self.get_entity("media_player.sonos_living_room")
            self.my_enitity.call_service("play_media", media_content_id = playListURL, media_content_type = "music")
            self.my_enitity.call_service("shuffle_set", shuffle = True)
            self.my_enitity.call_service("volume_set", volume_level = 0.1)
        except:
	        str = f"Cannot start SONOS Spotify playlist url: {playListURL}"
	        self.log(str, ascii_encode=False)
        str = f"started SONOS Spotify playlist url: {playListURL}"
        self.log(str, ascii_encode=False)
        
    def StopMusic(self, kwargs):
        self.my_enitity = self.get_entity("media_player.sonos_living_room")
        self.my_enitity.call_service("media_stop")
        str = f"Stopped Sonos"
        self.log(str, ascii_encode=False)
        
    def trigger_event(self):
        #Trigger music events only when TV is off
        if at_home_event.wait() and self.tv_enitity.getstate() == "off":
            return True
        else:
            return False
        
    def getplaylist(self):
        self.log("Getting playlist based on weather: %s", self.get_state("weather.barney_home_automation"))
        match self.get_state("weather.barney_home_automation"):
            case "cloudy":
                return playlist_cloudy_day
                
            case "fog":
                return playlist_cloudy_day
                
            case "partlycloudy":
                return playlist_cloudy_day
                
            case "rainy":
                return playlist_rainy_day
                
            case "hail":
                return playlist_rainy_day
                
            case "lighting":
                return playlist_rainy_day
                
            case "lighting-rainy":
                return playlist_rainy_day
            
            case "pouring":
                return playlist_rainy_day
              
            case "snowy":
                return playlist_snow
                
            case "snowy-rainy":
                return playlist_snow
                
            case "windy":
                return playlist_winter
                
            case "exceptional":
                return playlist_sunny_day
                
            #Default case 
            case _:
                return playlist_evening_chill
                
        
	    
	        

	    
	        