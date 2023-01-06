import time
import json

class Locatie:
    def __init__(self,long,lat,acc,data=None):
        self.long = long
        self.lat = lat
        self.acc = acc
        if data is None:
            self.data=time.time()
        else:
            self.data = data
      
    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        try:
            json_dict = json.loads(json_str)
            return cls(**json_dict)
        except:
            return None