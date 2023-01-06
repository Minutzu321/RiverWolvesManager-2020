from PIL.ExifTags import TAGS, GPSTAGS

def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def convert_to_degress(value):

    d = value[0]
    m = value[1]
    s = value[2]

    return d + (m / 60.0) + (s / 3600.0)

def get_exif_data(img):

    exif_data = {}
    info = img._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data

def get_lat(exif_data):

    # print(exif_data)
    if 'GPSInfo' in exif_data:
        gps_info = exif_data["GPSInfo"]
        gps_latitude = get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = get_if_exist(gps_info, 'GPSLatitudeRef')
        if gps_latitude and gps_latitude_ref:
            lat = convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat
            lat = str(f"{lat:.{5}f}")
            return lat
    else:
        return None

def get_lon(exif_data):

    # print(exif_data)
    if 'GPSInfo' in exif_data:
        gps_info = exif_data["GPSInfo"]
        gps_longitude = get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = get_if_exist(gps_info, 'GPSLongitudeRef')
        if gps_longitude and gps_longitude_ref:
            lon = convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
            lon = str(f"{lon:.{5}f}")
            return lon
    else:
        return None

def get_date_time(exif_data):
    if 'DateTime' in exif_data:
        date_and_time = exif_data['DateTime']
        return date_and_time 