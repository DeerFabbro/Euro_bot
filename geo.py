COUNTRY_BOUNDS = [
    # Западная Европа
    {"country": "Португалия", "currency": "EUR", "lat": (36.9, 42.2), "lon": (-9.5, -6.2)},
    {"country": "Испания", "currency": "EUR", "lat": (36.0, 43.8), "lon": (-9.3, 3.3)},
    {"country": "Франция", "currency": "EUR", "lat": (42.3, 51.1), "lon": (-4.8, 8.2)},
    {"country": "Бельгия", "currency": "EUR", "lat": (49.5, 51.5), "lon": (2.5, 6.4)},
    {"country": "Нидерланды", "currency": "EUR", "lat": (50.7, 53.6), "lon": (3.3, 7.2)},
    {"country": "Люксембург", "currency": "EUR", "lat": (49.4, 50.2), "lon": (5.7, 6.5)},
    {"country": "Великобритания", "currency": "GBP", "lat": (49.9, 60.9), "lon": (-8.2, 1.8)},
    {"country": "Ирландия", "currency": "EUR", "lat": (51.4, 55.4), "lon": (-10.5, -6.0)},
    {"country": "Германия", "currency": "EUR", "lat": (47.3, 55.1), "lon": (5.9, 15.1)},
    {"country": "Швейцария", "currency": "CHF", "lat": (45.8, 47.8), "lon": (5.9, 10.5)},
    {"country": "Австрия", "currency": "EUR", "lat": (46.4, 49.0), "lon": (9.5, 17.2)},
    {"country": "Италия", "currency": "EUR", "lat": (35.5, 47.1), "lon": (6.6, 18.5)},
    {"country": "Мальта", "currency": "EUR", "lat": (35.8, 36.1), "lon": (14.2, 14.6)},

    # Северная Европа
    {"country": "Норвегия", "currency": "NOK", "lat": (57.9, 71.2), "lon": (4.5, 31.1)},
    {"country": "Швеция", "currency": "SEK", "lat": (55.3, 69.1), "lon": (11.1, 24.2)},
    {"country": "Дания", "currency": "DKK", "lat": (54.6, 57.8), "lon": (8.1, 15.2)},
    {"country": "Финляндия", "currency": "EUR", "lat": (59.8, 70.1), "lon": (19.5, 31.6)},
    {"country": "Исландия", "currency": "ISK", "lat": (63.4, 66.6), "lon": (-24.5, -13.5)},
    {"country": "Эстония", "currency": "EUR", "lat": (57.5, 59.7), "lon": (21.8, 28.2)},
    {"country": "Латвия", "currency": "EUR", "lat": (55.7, 57.9), "lon": (21.0, 28.2)},
    {"country": "Литва", "currency": "EUR", "lat": (53.9, 56.5), "lon": (21.0, 26.8)},

    # Центральная Европа
    {"country": "Польша", "currency": "PLN", "lat": (49.0, 54.9), "lon": (14.1, 24.2)},
    {"country": "Чехия", "currency": "CZK", "lat": (48.5, 51.1), "lon": (12.1, 18.9)},
    {"country": "Словакия", "currency": "EUR", "lat": (47.7, 49.6), "lon": (16.8, 22.6)},
    {"country": "Венгрия", "currency": "HUF", "lat": (45.7, 48.6), "lon": (16.1, 22.9)},
    {"country": "Словения", "currency": "EUR", "lat": (45.4, 46.9), "lon": (13.4, 16.6)},
    {"country": "Хорватия", "currency": "EUR", "lat": (42.4, 46.6), "lon": (13.5, 19.4)},
    {"country": "Босния и Герцеговина", "currency": "BAM", "lat": (42.6, 45.3), "lon": (15.7, 19.7)},
    {"country": "Сербия", "currency": "RSD", "lat": (42.2, 46.2), "lon": (18.8, 23.0)},
    {"country": "Черногория", "currency": "EUR", "lat": (41.9, 43.6), "lon": (18.4, 20.4)},
    {"country": "Северная Македония", "currency": "MKD", "lat": (40.9, 42.4), "lon": (20.5, 23.0)},
    {"country": "Албания", "currency": "ALL", "lat": (39.6, 42.7), "lon": (19.3, 21.1)},

    # Восточная Европа
    {"country": "Беларусь", "currency": "BYN", "lat": (51.3, 56.2), "lon": (23.2, 32.8)},
    {"country": "Украина", "currency": "UAH", "lat": (44.4, 52.4), "lon": (22.1, 40.2)},
    {"country": "Молдова", "currency": "MDL", "lat": (45.5, 48.5), "lon": (26.6, 30.2)},
    {"country": "Румыния", "currency": "RON", "lat": (43.6, 48.3), "lon": (20.3, 29.7)},
    {"country": "Болгария", "currency": "BGN", "lat": (41.2, 44.2), "lon": (22.4, 28.6)},
    {"country": "Греция", "currency": "EUR", "lat": (34.8, 41.8), "lon": (19.4, 29.6)},

    # Кавказ
    {"country": "Грузия", "currency": "GEL", "lat": (41.1, 43.6), "lon": (40.0, 46.7)},
    {"country": "Армения", "currency": "AMD", "lat": (38.8, 41.3), "lon": (43.4, 46.6)},
    {"country": "Азербайджан", "currency": "AZN", "lat": (38.4, 41.9), "lon": (44.8, 50.6)},

    # Ближний Восток / Турция
    {"country": "Турция", "currency": "TRY", "lat": (35.8, 42.1), "lon": (26.0, 44.8)},
    {"country": "Израиль", "currency": "ILS", "lat": (29.5, 33.3), "lon": (34.3, 35.9)},

    # Россия (европейская часть + азиатская)
    {"country": "Россия", "currency": "RUB", "lat": (41.2, 82.0), "lon": (19.6, 180.0)},
]


def get_country_by_coords(lat: float, lon: float) -> dict | None:
    for entry in COUNTRY_BOUNDS:
        lat_min, lat_max = entry["lat"]
        lon_min, lon_max = entry["lon"]
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return {"country": entry["country"], "currency": entry["currency"]}
    return None


def get_coords_from_exif(image_bytes: bytes):
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
        import io

        img = Image.open(io.BytesIO(image_bytes))
        exif_data = img._getexif()
        if not exif_data:
            return None

        gps_info = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag)
            if tag_name == "GPSInfo":
                for gps_tag, gps_value in value.items():
                    gps_info[GPSTAGS.get(gps_tag)] = gps_value

        if not gps_info:
            return None

        def to_degrees(value):
            d, m, s = value
            return float(d) + float(m) / 60 + float(s) / 3600

        lat = to_degrees(gps_info["GPSLatitude"])
        lon = to_degrees(gps_info["GPSLongitude"])

        if gps_info.get("GPSLatitudeRef") == "S":
            lat = -lat
        if gps_info.get("GPSLongitudeRef") == "W":
            lon = -lon

        return {"lat": lat, "lon": lon}
    except Exception:
        return None