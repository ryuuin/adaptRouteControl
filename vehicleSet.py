#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import optparse
import random
import os
import sys
# route文件开头
rou_start = open("BProu_start.rou.xml", "w")
print("""<?xml version="1.0" encoding="UTF-8"?>
<routes>
    <vType id="typeA" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
    <vType id="typeB" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>""", file=rou_start)
rou_start.close()
rou_route = open("BProu_route.rou.xml", "w")
rou_vehicle = open("BProu_vehicle.rou.xml", "w")


N = 6000
namda = 3. / 10
pWE = namda
pEW = namda
pNS = namda
pSN = namda

e_virtual = 0.1
veh_num = 0

destin_list = ["E3", "E4", "W3", "W4", "N3", "N4", "S3", "S4"]
edge_name = ['11', '12', '13', '14', '15', '16', '21', '22', '23', '24', '25', '26', '31', '32', '33', '34',
              '35', '36', '41', '42', '43', '44', '45', '46', '51', '52', '53', '54', '55', '56', '61', '62',
              '63', '64', '65', '66']
destin_pressure = dict.fromkeys(destin_list)  # destinations
for d in destin_pressure:
    destin_pressure[d] = dict.fromkeys(edge_name)  # every junction of every destination
    for edge in edge_name:
        destin_pressure[d][edge] = [[], [], [], []]   # every junction has four edges: pressure(ve_number) of every edge

for i in range(N):
    if random.uniform(0, 1) < pWE:     # 随机生成WE方向的车辆
        start = random.randint(3, 4)
        final = random.randint(3, 4)
        v0 = str(0)+str(start)
        v_dst = str(7)+str(final)
        edge_str = v0 + "_" + "1" + str(start)
        print('    <route id="route%d" edges="%s"/>' % (veh_num, edge_str), file=rou_route)
        if random.uniform(0, 1) < 0.9:
            print('    <vehicle id="E%d_%i" type="typeA" route="route%d" depart="%i" />' % (
                final, veh_num, veh_num, i), file=rou_vehicle)
        else:
            print('    <vehicle id="E%d_%i" type="typeB" route="route%d" depart="%i" />' % (final, veh_num, veh_num, i),
                  file=rou_vehicle)
        veh_num += 1
    if random.uniform(0, 1) < pEW:     # 随机生成EW方向的车辆
        start = random.randint(3, 4)
        final = random.randint(3, 4)
        v0 = str(7)+str(start)
        v_dst = str(0)+str(final)
        edge_str = v0 + "_" + "6" + str(start)
        print('    <route id="route%d" edges="%s"/>' % (veh_num, edge_str), file=rou_route)
        if random.uniform(0, 1) < 0.9:
            print('    <vehicle id="W%d_%i" type="typeA" route="route%d" depart="%i" />' % (
                final, veh_num, veh_num, i), file=rou_vehicle)
        else:
            print('    <vehicle id="W%d_%i" type="typeB" route="route%d" depart="%i" />' % (final, veh_num, veh_num, i),
                  file=rou_vehicle)
        veh_num += 1
    if random.uniform(0, 1) < pNS:     # 随机生成NS方向的车辆
        start = random.randint(3, 4)
        final = random.randint(3, 4)
        v0 = str(start) + str(7)
        v_dst = str(final) + str(0)
        edge_str = v0 + "_" + str(start) + "6"
        print('    <route id="route%d" edges="%s"/>' % (veh_num, edge_str), file=rou_route)
        if random.uniform(0, 1) < 0.9:
            print('    <vehicle id="S%d_%i" type="typeA" route="route%d" depart="%i" />' % (
                final, veh_num, veh_num, i), file=rou_vehicle)
        else:
            print('    <vehicle id="S%d_%i" type="typeB" route="route%d" depart="%i" />' % (final, veh_num, veh_num, i),
                  file=rou_vehicle)
        veh_num += 1
    if random.uniform(0, 1) < pSN:     # 随机生成SN方向的车辆
        start = random.randint(3, 4)
        final = random.randint(3, 4)
        v0 = str(start) + str(0)
        v_dst = str(final) + str(7)
        edge_str = v0 + "_" + str(start) + "1"
        print('    <route id="route%d" edges="%s"/>' % (veh_num, edge_str), file=rou_route)
        if random.uniform(0, 1) < 0.9:
            print('    <vehicle id="N%d_%i" type="typeA" route="route%d" depart="%i" />' % (
                final, veh_num, veh_num, i), file=rou_vehicle)
        else:
            print('    <vehicle id="N%d_%i" type="typeB" route="route%d" depart="%i" />' % (final, veh_num, veh_num, i),
                  file=rou_vehicle)
        veh_num += 1


print("""<routes/>""", file=rou_vehicle)
rou_route.close()
rou_vehicle.close()
filename = ['BProu_start.rou.xml', 'BProu_route.rou.xml', 'BProu_vehicle.rou.xml']
with open('BProute.rou.xml', 'w') as outfile:
    for f in filename:
        with open(f) as infile:
            for line in infile:
                outfile.write(line)
outfile.close()

