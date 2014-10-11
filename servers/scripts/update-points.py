#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddnet import *
import sys
import os
from cgi import escape
from urllib import quote_plus
from time import sleep
from datetime import datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf8')

con = mysqlConnect()

types = sys.argv[1:]

with con:
  cur = con.cursor()
  cur.execute("set names 'utf8';")

  for type in types:
    f = open("types/%s/maps" % type, 'r')
    for line in f:
      words = line.rstrip('\n').split('|')
      if len(words) == 0 or not words[0].isdigit():
        continue

      stars = int(words[0])
      points = globalPoints(type, stars)

      mapName = words[1]
      #if len(words) > 2:
      #  mapperName = words[2]
      #else:
      #  mapperName = ""

      cur.execute("INSERT INTO record_maps(Map, Server, Points, Stars) VALUES ('%s', '%s', '%d', '%d') ON duplicate key UPDATE Server=VALUES(Server), Points=VALUES(Points), Stars=VALUES(Stars);" % (con.escape_string(mapName), con.escape_string(type), points, stars))
