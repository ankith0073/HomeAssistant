import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

class NotifyAnkithSushi(hass.Hass):
    def initialize(self):
        #Waste collection entities
        self.restmuell = self.get_entity("sensor.restmuell_waste")
        self.papier = self.get_entity("sensor.paper_waste")
        self.bio = self.get_entity("sensor.bio_waste")
        
        runtime = datetime.time(18, 00, 0)
        self.run_daily(self.check_waste_schedule, runtime)
        
    def check_waste_schedule(self, kwargs):
        if self.restmuell.is_state("Restmüll in 1 days"):
            self.log("Notify for restmüll")
            self.notify_restmuell()
            
        if self.papier.is_state("Papier in 1 days"):
            self.log("Notify for papier")
            self.notify_papier()
            
        if self.bio.is_state("Biomüll in 1 days"):
            self.log("Notify for biomüll")
            self.notify_bio()
   
    def notify_restmuell(self):
        self.call_service("notify/mobile_app_iphone_barney", title = "Restmüll tomorrow", message = "Please keep restmüll outside")
        self.call_service("notify/mobile_app_iphone", title = "Restmüll tomorrow", message = "Please keep restmüll outside")
        
    def notify_papier(self):
        self.call_service("notify/mobile_app_iphone_barney", title = "Papier tomorrow", message = "Please keep Papier outside")
        self.call_service("notify/mobile_app_iphone", title = "Papier tomorrow", message = "Please keep Papier outside")
        
    def notify_bio(self):
        self.call_service("notify/mobile_app_iphone_barney", title = "Biomüll tomorrow", message = "Please keep Biomüll outside")
        self.call_service("notify/mobile_app_iphone", title = "Biomüll tomorrow", message = "Please keep Biomüll outside")
        
