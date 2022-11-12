import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

class KitchenLight(hass.Hass):
    def initialize(self):
        self.my_enitity = self.get_entity("binary_sensor.kitchen_motion_sensor")
        self.sun_entity = self.get_entity("sun.sun")
        self.my_enitity.listen_state(self.kitchen_light_on, new = "on")
        self.my_enitity.listen_state(self.kitchen_light_off, new = "off")
        
    def kitchen_light_on(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():
            self.my_enitity = self.get_entity("light.controller_rgb_ir_fdb53b")
            self.my_enitity.call_service("turn_on",rgb_color = [254, 255, 0], brightness = 80)
            str = f"Turning on Kitchen lights"
            self.log(str, ascii_encode=False)
        
    def kitchen_light_off(self,  entity, attribute, old, new, kwargs):
        self.my_enitity = self.get_entity("light.controller_rgb_ir_fdb53b")
        self.my_enitity.call_service("turn_off")
        str = f"Turning off Kitchen lights"
        self.log(str, ascii_encode=False)
        
    def trigger_event(self):
        #Trigger only when home and after sunset
        if at_home_event.wait() and self.sun_entity.is_state('below_horizon'):
            return True
        else:
            return False
        