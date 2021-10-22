
import json

class Medicion:
    def __init__(self,id, latitud, longitud, co2, fecha, hora):
        self.id = id
        self.latitud = latitud
        self.longitud = longitud
        self.co2 = co2
        self.fecha = fecha
        self.hora = hora

## Convierte la clase Medicion en JSON (string)
    def toJson(self):
        json = {
            "id": self.id,
            "latitud": self.latitud,
            "longitud":self.longitud,
            "co2": self.co2,
            "fecha": "{}".format(self.fecha),
            "hora":"{}".format(self.hora),
            }
        return json