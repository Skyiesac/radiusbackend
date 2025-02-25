import json
import math
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import FileUploaded
from django.contrib.gis.db.models.functions import Distance

# def haversine_distance(lat1, lon1, lat2, lon2):
#     """
#     Calculate the great circle distance between two points
#     on the earth (specified in decimal degrees)
#     """
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = (
#         math.sin(dlat / 2) ** 2
#         + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
#     )
#     c = 2 * math.asin(math.sqrt(a))
#     r = 6371  # Radius of earth in kilometers
#     return c * r * 1000  # Convert to meters


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):

        try:
            data = json.loads(text_data)

            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if not latitude or not longitude:
                await self.send(text_data=json.dumps({"error": "Invalid coordinates"}))
                return

            # Create point from user coordinates
            user_point = Point(longitude, latitude, srid=4326)

            # Efficient nearby file query using PostGIS spatial lookup
            nearby_files = (
                FileUploaded.objects.filter(
                    location__distance_lte=(user_point, D(m=100))
                )
                .annotate(distance=Distance("location", user_point))
                .values("id", "name", "distance")
            )

            await self.send(text_data=json.dumps({"nearby_files": list(nearby_files)}))

        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))
