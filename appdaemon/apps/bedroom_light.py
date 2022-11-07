import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

class BedroomLight(hass.Hass):
    def initialize(self):
        self.my_enitity = self.get_entity("binary_sensor.bedroom_motion_sensor")
        self.sun_entity = self.get_entity("sun.sun")
        self.my_enitity.listen_state(self.bedroom_light_on, new = "on")
        self.my_enitity.listen_state(self.bedroom_light_off, new = "off")
        
    def bedroom_light_on(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():
            self.my_enitity = self.get_entity("light.bedroom_lamp")
            self.my_enitity.call_service("turn_on", brightness = 40)
            str = f"Turning on bedroom lights"
            self.log(str, ascii_encode=False)
        
    def bedroom_light_off(self,  entity, attribute, old, new, kwargs):
        self.my_enitity = self.get_entity("light.bedroom_lamp")
        self.my_enitity.call_service("turn_off")
        str = f"Turning off bedroom lights"
        self.log(str, ascii_encode=False)
        
    def trigger_event(self):
        if at_home_event.wait() and self.sun_entity.is_state('below_horizon') and self.now_is_between("sunset", "23:00:00"):
            return True
        else:
            return False
        
        