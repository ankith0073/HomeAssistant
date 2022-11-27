import appdaemon.plugins.hass.hassapi as hass
import datetime
import time

class MusicSnapshot(hass.Hass):
    def initialize(self):
        entity_name = "media_player.samsung_7_series_55"
        self.media_entity = "media_player.sonos_living_room"
        self.my_enitity = self.get_entity(entity_name)
        self.my_enitity.listen_state(self.music_snapsnotcb, new = "on")
        self.my_enitity.listen_state(self.music_restorecb, new = "off")
        
    def music_snapsnotcb(self, entity, attribute, old, new, kwargs):
        self.log("Creating Sonos snapshot")
        self.sonos_enitity = self.get_entity(self.media_entity)
        #self.log(self.list_services())
        self.call_service("sonos/snapshot", entity_id = self.media_entity)
        self.sonos_enitity.call_service("media_pause")
        self.log_state_change(entity_name = self.media_entity)
        
    def music_restorecb(self, entity, attribute, old, new, kwargs):
        #Restore only until 23:00:00
        if self.now_is_between(start_time = "08:00:00", end_time = "23:00:00"):
            self.log("Restoring Sonos snapshot")
            self.call_service("sonos/restore", entity_id = self.media_entity)
            self.sonos_enitity = self.get_entity(self.media_entity)
            self.sonos_enitity.call_service("media_play")
            self.log_state_change(entity_name = self.media_entity)
        
    def log_state_change(self, entity_name = ""):
        time.sleep(1)
        str = f"Entity {entity_name} state change to {self.get_entity(entity_name).get_state()}"
        self.log(str, ascii_encode=False)
        
            