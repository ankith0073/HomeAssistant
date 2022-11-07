import appdaemon.plugins.hass.hassapi as hass
import datetime
from threading import Event
import typing
import time

at_home_event = Event()
away_from_home_event = Event()

class AtHomeTrigger(hass.Hass):
    def initialize(self):
        self.ankith_home = False
        self.sushi_home = False
        
        #State change flag for logging purposes
        self._state_change = False
        
        self.my_enitity = self.get_entity("device_tracker.iphone_barney_2")
        self.sushi_enitity = self.get_entity("device_tracker.sushi_iphone")
        
        self.my_enitity.listen_state(self.ankith_at_home, new = "home")
        self.my_enitity.listen_state(self.ankith_away_home, new = "not_home")
        
        self.sushi_enitity.listen_state(self.sushi_at_home, new = "home")
        self.sushi_enitity.listen_state(self.sushi_away_home, new = "not_home")
        
        #check if someone is home every 5 seconds
        
        #Turn on needs to be faster for luxury feeling
        self.run_every(self.turn_on_automations, "now", interval = 2)
        
        #Turn off can be slower
        self.run_every(self.turn_off_automations, "now", interval = 3)
        
    @property
    def state_change(self):
        return self._state_change

    @state_change.setter
    def state_change(self, value: bool):
        self._state_change = value
        
    def ankith_at_home(self,  entity, attribute, old, new, kwargs):
        self.log("Barney Iphone is connected to WIFI")
        self.ankith_home = True
        self.state_change = True
        self.log("ankith_home set to " + str(self.ankith_home))
        
    def ankith_away_home(self,  entity, attribute, old, new, kwargs):
        self.log("Barney Iphone disconnected to WIFI")
        self.ankith_home = False
        self.state_change = True
        self.log("ankith_home set to " + str(self.ankith_home))
        
    def sushi_at_home(self,  entity, attribute, old, new, kwargs):
        self.log("Sushi Iphone is connected to WIFI")
        self.sushi_home = True
        self.state_change = True
        self.log("Sushi_home set to " + str(self.sushi_home))
        
    def sushi_away_home(self,  entity, attribute, old, new, kwargs):
        self.log("Sushi Iphone disconnected to WIFI")
        self.sushi_home = False
        self.state_change = True
        self.log("Sushi_home set to " + str(self.sushi_home))
        
    def turn_on_automations(self,  kwargs):
        if self.ankith_home or self.sushi_home:
            at_home_event.set()
            away_from_home_event.clear()
        if self.state_change:
            time.sleep(2)
            self.log("ankith home: " + str(self.ankith_home) + " sushi_home: " + str(self.sushi_home))
            self.log("Event at_home_event :" + str(at_home_event.is_set()))
            self.state_change = False
        
    def turn_off_automations(self,   kwargs):
        if not(self.ankith_home) and not(self.sushi_home):
            at_home_event.clear()
            away_from_home_event.set()
        if self.state_change:
            time.sleep(2)
            self.log("ankith home: " + str(self.ankith_home) + " sushi_home: " + str(self.sushi_home))
            self.log("Event at_home_event :" + str(at_home_event.is_set()))
            self.state_change = False