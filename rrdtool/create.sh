#!/usr/bin/env bash

rrdtool create temperature.rrd \
  --start 1460206901 --step 5  \
  DS:int_temp:GAUGE:3700:U:U \
  RRA:AVERAGE:0.5:1:17280  \
  RRA:AVERAGE:0.5:12:43200 \
  RRA:AVERAGE:0.5:720:8760  \
  RRA:AVERAGE:0.5:5760:10950
