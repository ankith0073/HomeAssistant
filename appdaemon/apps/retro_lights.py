import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event


class RetroLightOn(hass.Hass):
    def initialize(self):
        self.run_at_sunset(self.TurnOnLight)
        runtime = datetime.time(23, 00, 00)
        handle = self.run_daily(self.TurnOffLight, runtime)
        
    def TurnOnLight(self, kwargs):
        if at_home_event.wait():
            self.log("Turning retro lights on")
            self.log("Event at_home_event :" + str(at_home_event.is_set()))
            self.turn_on('light.retro_light_1', brightness = 35, transition = 3)
            self.turn_on('light.retro_light_2', brightness = 35, transition = 3)
            self.turn_on('light.retro_light_3', brightness = 35, transition = 3)
        
    def TurnOffLight(self, kwargs):
        self.log("Turning retro lights off")
        self.turn_off('light.retro_light_1', transition = 3)
        self.turn_off('light.retro_light_2', transition = 3)
        self.turn_off('light.retro_light_3', transition = 3)
        
        
        
