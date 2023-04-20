def process_hotels_data(data):
    hotels = []
    for item in data["results"]:
        hotel = {
            "id": item["id"],
            "name": item["name"],
            "address": item["address"],
            "rating": item["rating"],
            "price": item["price"],
            "coordinates": (item["latitude"], item["longitude"]),
        }
        hotels.append(hotel)
    return hotels
