#!/usr/bin/env python

__author__ = 'LEllingwood'

import requests
import sys
import argparse
import turtle
import time


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--astronaut',
                        help="list the astronauts", action='store_true')
    parser.add_argument(
        '-g', '--geo', help="find longitute and latitude ", action='store_true')
    parser.add_argument('-m', '--mark_station',
                        help="mark station and Indy", action='store_true')
    return parser


def ast_name():
    url = 'http://api.open-notify.org/astros.json'
    r = requests.get(url).json()
    # print(r)
    print("Number of Astronauts: " + str((r["number"])) + "\n")

    for each in r["people"]:
        print("Astronaut: " + each["name"] +
              ": " + "Craft: " + each["craft"] + "\n")


def geo_coord():
    url = "http://api.open-notify.org/iss-now.json"
    r = requests.get(url).json()
    print("Timestamp: " + str(r["timestamp"]))
    print("ISS Position: " + "Latitude: " +
          str(r["iss_position"]["latitude"]) + " Longitude: " + str(r["iss_position"]["longitude"]))
    return r


def mark_station():
    r = geo_coord()
    # print r
    # Set up screen
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic("map.gif")
    screen.register_shape('iss.gif')
    # Turtle
    station = turtle.Turtle()
    station.shape('iss.gif')
    station.setheading(90)

    # # go to station
    station.penup()
    station.goto(float(r['iss_position']['longitude']),
                 float(r['iss_position']['latitude']))

    # when will iss pass over indy
    payload = {'lat': 39.7684, 'lon': -86.1581}
    indy = requests.get('http://api.open-notify.org/iss-pass.json', params=payload).json()
    indy_time = indy["response"][0]["risetime"]
    indy_converted_time = time.ctime(indy_time)
    print("Time the iss will be over Indy: " + indy_converted_time)
    
    # find indy with a dot
    yellow_dot = turtle.Turtle()
    yellow_dot.shape('circle')
    yellow_dot.color('yellow')
    yellow_dot.turtlesize(1)
    yellow_dot.penup()
    yellow_dot.goto(payload['lon'], payload['lat'])
    screen.exitonclick()


def main(args):
    parser = create_parser()
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    if args.astronaut:
        return ast_name()

    if args.geo:
        r = geo_coord()

    if args.mark_station:
        pass
        mark_station()


if __name__ == '__main__':
    main(sys.argv[1:])
