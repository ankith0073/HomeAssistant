import appdaemon.plugins.hass.hassapi as hass

class SpeakerSnapshotwhenTVOn(hass.Hass):
    def initialize(self):
        self.my_entity = self.get_entity("media_player.samsung_7_series_55")
        self.listen_state(self.SpeakerCallback)
        
    def SpeakerCallback(self, entity, attribute, old, new, kwargs):
        if(self.my_entity.is_state("on")):
            self.log("Log Test: TV is on")
        else:
            self.log("Log Test: TV is off")
            self.log( self.time())
            self.log(self.get_now())
            self.log(self.now_is_between("23:00:00", "23:20:00"))