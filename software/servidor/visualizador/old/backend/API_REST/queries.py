from bson.son import SON
from datetime import timedelta,datetime


class Queries(object):
    @staticmethod
    def get_boats(matricula, point, max_distance, minutes):
        return {
            "geometry": SON([("$near", {
                "$geometry": SON([("type", "Point"), ("coordinates", point)]),
                "$maxDistance": max_distance
            })]),
            "properties.hora": {
                "$gt": datetime.utcnow() - timedelta(minutes=minutes),
                "$lt": datetime.utcnow() + timedelta(minutes=minutes)
            },
            "matricula": { "$ne": matricula}
        }
