#!/usr/bin/python3
import os
import pandas as pd
import sys
import utm

assert len(sys.argv) == 2

df = pd.read_csv(sys.argv[1])

# Strip whitespace from column headers
df.rename(inplace=True, columns=lambda x: x.strip())

# Get UTM coordinates
x = []
y = []
zone = []
for lat, lon in zip(df['lat'], df['lon']):
    easting, northing, zone_number, zone_letter = utm.from_latlon(lat, lon)

    # Save in mm
    x.append(easting * 1000)
    y.append(northing * 1000)

    zone.append('%d%s' % (zone_number, zone_letter))
df['X [mm]'] = x
df['Y [mm]'] = y
df['UTM zone'] = zone

df['altitude'] *= 1000  # Convert to mm

# Rename the columns to correspond to what we use elsewhere + tidiness
df.rename(inplace=True, columns={
          'gps quality': 'GPS quality', 'lat': 'Latitude', 'lon': 'Longitude',
          'altitude': 'Z [mm]', 'roll': 'Roll [degrees]',
          'pitch': 'Pitch [degrees]', 'yaw': 'Heading [degrees]',
          'image name': 'Filename', 'timestamp': 'Timestamp [ms]'})

# Reorder for clarity
df = df.reindex(columns=[
    'Timestamp [ms]', 'X [mm]', 'Y [mm]', 'Z [mm]', 'Heading [degrees]',
    'Pitch [degrees]', 'Roll [degrees]', 'Filename', 'GPS quality', 'UTM zone'])

# Output to stdout
print(df.to_csv(index=False))
