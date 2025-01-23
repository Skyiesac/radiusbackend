import json
import math

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import FileUploaded


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r * 1000  # Convert to meters


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user_latitude = data.get("latitude")
            user_longitude = data.get("longitude")

            # Validate coordinates
            if not user_latitude or not user_longitude:
                await self.send(
                    text_data=json.dumps(
                        {
                            "error": "Invalid coordinates",
                        },
                    ),
                )
                return

            if data.get("latitude"):
                if data["latitude"] < -90 or data["latitude"] > 90:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "error": "Invalid coordinates",
                            },
                        ),
                    )
                return

            if data.get("longitude"):
                if data["longitude"] < -180 or data["longitude"] > 180:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "error": "Invalid coordinates",
                            },
                        ),
                    )
                return

            # Find nearby files
            nearby_files = []
            for file in FileUploaded.objects.all():
                distance = haversine_distance(
                    user_latitude,
                    user_longitude,
                    file.latitude,
                    file.longitude,
                )

                # Check if file is within 100 meters
                if distance <= 100:
                    nearby_files.append(
                        {
                            "id": file.id,
                            "name": file.name,
                            "distance": round(distance, 2),
                        },
                    )

            # Send nearby files
            await self.send(
                text_data=json.dumps(
                    {
                        "nearby_files": nearby_files,
                    },
                ),
            )

        except json.JSONDecodeError:
            await self.send(
                text_data=json.dumps(
                    {
                        "error": "Invalid JSON",
                    },
                ),
            )
        except Exception as e:
            await self.send(
                text_data=json.dumps(
                    {
                        "error": str(e),
                    },
                ),
            )
