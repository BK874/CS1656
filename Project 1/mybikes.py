# Brian Knotten
# CS 1656
# Project 1

import argparse as argp
from requests import get
import json
import math

# mybikes.py accesses live data from the HealthyRidePGH website and provides
# specific answers to specific queries about shared bike availability in the
# Pittsburgh region.
# Invoked as: python3 mybikes.py baseURL command [parameters]
# Data feeds:
# Station Information (https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_information.json)
# Station Status (https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_status.json)

# Helper functions
def distance(lat1, lon1, lat2, lon2):
    p = math.pi/180
    a = 0.5 - math.cos((lat2-lat1)*p)/2+math.cos(lat1*p)*math.cos(lat2*p)* \
        (1-math.cos((lon2-lon1)*p))/2
    return 12742 * math.asin(math.sqrt(a))

def minDistance(coords, loc):
    return min(coords, key=lambda p:
               distance(float(loc['lat']), float(loc['lon']), float(p['lat']),
                        float(p['lon'])))

def minThreeDist(coords, loc):
    min1 = minDistance(coords, loc)
    coords2 = removeKey(coords, min1)
    min2 = minDistance(coords2, loc)
    coords3 = removeKey(coords2, min2)
    min3 = minDistance(coords3, loc)
    return [min1, min2, min3]

def removeKey(c, key):
    d = c.copy()
    d.remove(key)
    return d

# Process the input (url and commands)
parser = argp.ArgumentParser()
parser.add_argument("url", help = "the data feed")
parser.add_argument("command", help = "the desired command")
parser.add_argument("id_latitude", nargs = '?', help = "the station id or latitude")
parser.add_argument("longitude", type = float, nargs = '?', help = "the longitude")
args = parser.parse_args()
if args.id_latitude == None:
    args.id_latitude = ""
if args.longitude == None:
    args.longitude = ""

# Command 1: total_bikes
# Computes number of bikes currently available over all stations in the
# entire HealthyRidePGH network.
# Invoke: python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_bikes
# Sample output: Command=total_bikes \n Parameters= \n Output=123
if args.command == "total_bikes":
    response = get(args.url+'station_status.json')
    station_status = json.loads(response.content)
    #Dictionary contain 3 items: time last updated, time till updated,
    #and data - a dictionary containing an array of stations (what we want)
    #The array contains the id, bikes available, docks available, installation
    #status, renting status, return status, and time last reported
    total_bikes_avail = 0
    for station in range(len(station_status['data']['stations'])):
        total_bikes_avail += station_status['data']['stations'][station]\
            ['num_bikes_available']

    print("Command=" + args.command)
    print("Parameters=" + args.id_latitude + args.longitude)
    print("Output=" + str(total_bikes_avail))

# Command 2: total_docks
# Computes the number of docks currently available over all stations in the
# entire HealthyRidePGH network.
# Invoke: python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_docks
# Sample output: Command=total_docks \n Parameters= \n Output=168
elif args.command == "total_docks":
    response = get(args.url+'station_status.json')
    station_status = json.loads(response.content)
    total_docks_avail = 0
    for station in range(len(station_status['data']['stations'])):
        total_docks_avail += station_status['data']['stations'][station]\
            ['num_docks_available']

    print("Command=" + args.command)
    print("Parameters=" + args.id_latitude + args.longitude)
    print("Output=" + str(total_docks_avail))
    
# Command 3: percent_avail
# Computes number of docks currently available for a specified station as
# a perecentage over the total number of bikes and docks available.
# Parameter: station_id
# Invoke: python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ percent_avail 342885
# Sample output: Command=percent_avail \n Parameters=342885 \n Output=76%
elif args.command == "percent_avail":
    if args.id_latitude == "":
        print("Parameter <station id number> is required")
    else:
        response = get(args.url+'station_status.json')
        station_status = json.loads(response.content)
        station = next(stat for stat in station_status['data']['stations'] if
                       stat['station_id'] == args.id_latitude)
        bikes_avail = station['num_bikes_available']
        docks_avail = station['num_docks_available']
        perc_avail = math.floor(100 * (docks_avail/(bikes_avail + docks_avail)))
        print("Command=" + args.command)
        print("Parameters=" + args.id_latitude + args.longitude)
        print("Output=" + str(perc_avail) + "%")


# Command 4: closest_stations
# Returns the station_ids and names of the three closest HealthyRidePGH
# stations based just on latitude and longitude (of stations and specified location)
# Parameters: latitude longitude
# Invoke: python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_stations 40.444618 -79.954707
# Command=closest_stations \n Parameters=40.444618 -79.954707 \n Output= \n 342885, Schenley Dr at Schenley Plaza (Carnegie Library Main) \n 342887, Fifth Ave & S Dithridge St \n 342882, Fifth Ave & S Bouquet St
elif args.command == "closest_stations":
    if args.id_latitude == "" or args.longitude == "":
        print("Parameters <lat> and <lon> are required")
    else:
        response = get(args.url+'station_information.json')
        station_info = json.loads(response.content)
        loc = {'lat': args.id_latitude, 'lon': args.longitude}
        minDists = minThreeDist(station_info['data']['stations'], loc)
        print("Command=" + args.command)
        print("Parameters=" + str(args.id_latitude) + " " + str(args.longitude))
        print("Output=")
        for place in minDists:
            print(place['station_id']+ " " + place["name"])
        

# Command 5: closest_bike
# Returns the station_id and name of the closest HealthyRidePGH station that
# has available bikes, given a specific latitude and longitude.
# Parameters: latitude longitude
# Invoke: python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_bike 40.444618 -79.954707
# Sample output: Command=closest_bike \n Parameters=40.444618 -79.954707 \n Output=342887, Fifth Ave & S Dithridge St
elif args.command == "closest_bike":
    if args.id_latitude == "" or args.longitude == "":
        print("Parameters <lat> and <lon> are required")
    else:
        response = get(args.url+'station_information.json')
        response2 = get(args.url+'station_status.json')
        station_info = json.loads(response.content)
        station_status = json.loads(response2.content)
        #Create a list of all the stations that currently have bikes
        #and find the nearest one
        statWithBike = list(filter(lambda d: d['num_bikes_available'] > 0,
                                   station_status['data']['stations']))
        statWithBikeInfo = []
        for stat in station_info['data']['stations']: #equivalent lambda filter?
            for statBike in statWithBike:
                if stat['station_id'] == statBike['station_id']:
                    statWithBikeInfo.append(stat)
                
        loc = {'lat': args.id_latitude, 'lon': args.longitude}
        output = minDistance(statWithBikeInfo, loc)
        print("Command=" + args.command)
        print("Parameters=" + str(args.id_latitude) + " " + str(args.longitude))
        print("Output=" + output['station_id']+ " " + output["name"])

# Handle invalid commands
else:
    print("Not a valid command.")
    print("Valid commands (parameters in <>):")
    print("total_bikes")
    print("total_docks")
    print("percent_avail <station id number>")
    print("closest_stations <lat> <lon>")
    print("closest_bike <lat> <lon>")
