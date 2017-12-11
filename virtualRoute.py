#!/usr/bin/env python

"""

@file    runner.py

@author  Lena Kalleske

@author  Daniel Krajzewicz

@author  Michael Behrisch

@author  Jakob Erdmann

@date    2009-03-26

@version $Id: runner.py 22608 2017-01-17 06:28:54Z behrisch $



Tutorial for traffic light control via the TraCI interface.



SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/

Copyright (C) 2009-2017 DLR/TS, Germany



This file is part of SUMO.

SUMO is free software; you can redistribute it and/or modify

it under the terms of the GNU General Public License as published by

the Free Software Foundation; either version 3 of the License, or

(at your option) any later version.

"""

from __future__ import absolute_import

from __future__ import print_function

import os
import sys
import optparse
import random
import time
import math

# we need to import python modules from the $SUMO_HOME/tools directory
SUMO_HOME = "/usr/share/sumo/"

try:

    sys.path.append(os.path.join(os.path.dirname(

        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests

    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(

        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs

    from sumolib import checkBinary

except ImportError:

    sys.exit(

        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation "
        "(it should contain folders 'bin', 'tools' and 'docs')")

import traci


def get_options():
    optParser = optparse.OptionParser()

    optParser.add_option("--nogui", action="store_true",

                         default=False, help="run the commandline version of sumo")

    options, args = optParser.parse_args()

    return options


# f_path="data/compare(rho=0.1-1)lq/"
def get_minilink(node_n, node_d):
    lnum1 = abs(int(node_n[0])-int(node_d[0]))
    lnum2 = abs(int(node_n[1])-int(node_d[1]))
    res = lnum1+lnum2
    return res



f_path = "/home/liu/Documents/adapt-BP/pyCode/"
if not os.path.exists(f_path):
    os.makedirs(f_path)

f_staytime = open(f_path + "staytime_bp.txt", "wb")

# this is the main entry point of this script

if __name__ == "__main__":

    options = get_options()

    # this script has been called from the command line. It will start sumo as a

    # server, then connect and run

    # if options.nogui:

    #    sumoBinary = checkBinary('sumo')

    # else:

    #    sumoBinary = checkBinary('sumo-gui')


    # sumoBinary = checkBinary('sumo')
    sumoBinary = checkBinary('sumo-gui')

    rho = 0  # parameter controlling vehicle arrival rates
    run_num = 101                                                                              #101x5400s

    episode_num = run_num
    print('episode total: ', episode_num)
    junction_num = [1, 2, 3, 4, 5, 6]
    trafficlight_num = [1, 2, 3, 4, 5, 6]
    for i in range(episode_num):


        t0 = time.time()
        # this is the normal way of using traci. sumo is started as a
        # subprocess and then the python script connects and runs
        traci.start([sumoBinary, "-c", "/home/liu/Documents/adapt-BP/somoFile/ad_backpress.sumo.cfg",
                     "--tripinfo-output","tripinfo.xml"])

        # run()
        # four actions: 0 2 4 6
        phase = [0, 2, 4, 6]
        yellow = [1, 3, 5, 7]

        # destination record
        destination = ["E3", "E4", "W3", "W4", "N3", "N4", "S3", "S4"]  # destination name
        destin_junction = [str(7)+str(3), str(7)+str(4), str(0)+str(3), str(0)+str(4), str(3) + str(0), str(4) + str(0),
                           str(3) + str(7), str(4) + str(7)]
        start_edges = [str(7)+str(3)+"_"+str(6)+str(3),str(7)+str(4)+"_"+str(6)+str(4), str(0)+str(3)+"_"+str(1)+str(3)
            ,str(0) + str(4) + "_" + str(1) + str(4), str(3)+str(0)+"_"+str(3)+str(1), str(4)+str(0)+"_"+str(4)+str(1),
            str(3) + str(7) + "_" + str(3) + str(6), str(4)+str(7)+"_"+str(4)+str(6)]
        destin_dic = dict.fromkeys(destination)
        for k in xrange(0, 8):
            destin_dic[destination[k]] = destin_junction[k]

        action_duration = 15  # duration of actions, it is equal to the queen interval of traffic signals
        transition_duration = 4  # yellow duration

        edge_name = ['00','01','02','03','04','05','06','07','10','11', '12', '13', '14', '15', '16','17','20', '21',
                        '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34',
                        '35', '36', '37', '40', '41', '42', '43', '44', '45', '46', '47', '50', '51', '52', '53', '54',
                        '55', '56', '57', '60', '61', '62','63', '64', '65', '66', '67','70','71','72','73','74','75',
                        '76','77']
        trafficLight_edge = ['11', '12', '13', '14', '15', '16', '21', '22', '23', '24', '25', '26', '31', '32', '33', '34',
                     '35', '36', '41', '42', '43', '44', '45', '46', '51', '52', '53', '54', '55', '56', '61', '62',
                     '63', '64', '65', '66']

        # record virtual vehicle number of all edges
        viredge_name = ['00','01','02','03','04','05','06','07','10','11', '12', '13', '14', '15', '16','17','20', '21',
                        '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34',
                        '35', '36', '37', '40', '41', '42', '43', '44', '45', '46', '47', '50', '51', '52', '53', '54',
                        '55', '56', '57', '60', '61', '62','63', '64', '65', '66', '67','70','71','72','73','74','75',
                        '76','77']
        timer = dict.fromkeys(edge_name, 0)  # counts the time to decide the time agent should act
        timer_len = dict.fromkeys(edge_name, 0)
        previous_action = dict.fromkeys(edge_name, 0)
        action = dict.fromkeys(edge_name, 0)
        edge_dict = dict.fromkeys(edge_name)
        junction_phase = dict.fromkeys(edge_name) # record the phase of every junction
        junction_destin = dict.fromkeys(edge_name)  # record the chosen destination of every junction
        select_action = dict.fromkeys(edge_name, 1)  # whether need to choose phase
        # transition_phase = 0  # 1: if action is changed, then a transition phase follows; else, no transition phase
        transition_phase = dict.fromkeys(edge_name, 0)
        # dict for data storing
        vir_onroads = dict.fromkeys(viredge_name)  # number of virtual vehicles on all edges/roads
        virId_onroads = dict.fromkeys(edge_name)   # IDs of vehicles on all edges/roads
        enter_time = dict.fromkeys(edge_name)
        v_delay = dict.fromkeys(edge_name)
        v_num = dict.fromkeys(edge_name)
        v_staytime = dict.fromkeys(edge_name)
        veIdpre = dict.fromkeys(edge_name)
        destination_list = [0, 0, 0, 0, 0, 0, 0, 0]   # number of virtual vehicles of 8 destinations
        edgeli = dict.fromkeys(edge_name)
        for m in junction_num:
            for n in junction_num:
                jun_name = str(m)+str(n)
                edge_dict[str(m)+str(n)] = [str(m)+str(n-1)+'_'+str(m)+str(n), str(m-1)+str(n)+'_'+str(m)+str(n),
                                            str(m)+str(n+1)+'_'+str(m)+str(n), str(m+1)+str(n)+'_'+str(m)+str(n)]
                veIdpre[jun_name] = dict.fromkeys(edge_dict[jun_name], [])
                virId_onroads[str(m) + str(n)] = [[], [], [], []]   # IDs of vehicles on all edges/roads
                enter_time[str(m) + str(n)] = [[], [], [], []]
                v_delay[str(m) + str(n)] = [[], [], [], []]
                v_num[str(m) + str(n)] = [[], [], [], []]
                v_staytime[str(m) + str(n)] = [[], [], [], []]
                junction_phase[str(m) + str(n)] = phase

        for k in viredge_name:
            # number of virtual vehicles of 8 destinations on all edges/roads
            vir_onroads[k] = [destination_list, destination_list, destination_list, destination_list]
        sim_len = 5400

        # important note: set phase and simulationStep() should be paired
        for e in trafficLight_edge:
            tls_id = "N_"+e
            traci.trafficlights.setPhase(tls_id, 0)  # initialize phase to 0
        traci.simulationStep()  # execute one round first to align simulation time
        step = 0
        last_test_leave = []
        vehicle_gap = 9  # the space of each vehicle need
        u = 11
        pre_exTrans_r0 = dict.fromkeys(destination)
        pre_exTrans_r1 = dict.fromkeys(destination)
        pre_exTrans_r2 = dict.fromkeys(destination)
        pre_exTrans_r3 = dict.fromkeys(destination)
        for k in destination:   # right, ahead and left for three direction
            pre_exTrans_r0[k] = [u, u, u]
            pre_exTrans_r1[k] = [u, u, u]
            pre_exTrans_r2[k] = [u, u, u]
            pre_exTrans_r3[k] = [u, u, u]
        while step < sim_len:
            # print('******************** ')
            # agent selects action and sets phase


            # renew virtual vehicles queue
            # 1.check exogenous vehicles of starting queue, generate virtual vehicle
            vNumStart = dict.fromkeys(start_edges)  # to store ids of each virgin edge
            eVir = 1.15
            for k in vNumStart.keys():
                vNumStart[k] = []
            for k in vNumStart.keys():
                # get all the ids of vehicle on this virgin edge and get the destination
                # (first two characters) from ids
                vNumStart[k] = traci.edge.getLastStepVehicleIDs(k)
            for k in vNumStart.keys():
                for idVe in vNumStart[k]:  # for every id in  virgin edge
                    for m in junction_num:
                        for n in junction_num:
                            junc = str(m) + str(n)  # the current junction id
                            desN = idVe[0:2]  # find destination
                            desI = destination.index(desN)  # find destination index
                            if edge_dict[junc].count(k) != 0:
                                road_index = edge_dict[junc].index(k)
                                vir_onroads[junc][road_index][desI] += eVir  # generate virtual vehicle

            # back pressure algorithm
            # 1.calculate the difference
            for m in junction_num:
                for n in junction_num:
                    junc = str(m) + str(n)  # the current junction id
                    if select_action[junc] == 1:
                        road = [0, 1, 2, 3]
                        select_action[junc] = 0  # a:upstream  b:downstream   0,1,2,3:upstream edge
                        dif_vir = [[], [], [], []]
                        alfa = 2

                        # for every junction every road every destination
                        # need discuss

                        for d in xrange(8):
                            dif_vir[0].append(vir_onroads[junc][0][d] - vir_onroads[str(m + 1) + str(n)][0][d] + alfa*(get_minilink(junc,destin_junction[d])-get_minilink(str(m + 1) + str(n),destin_junction[d])))
                            dif_vir[1].append(vir_onroads[junc][1][d] - vir_onroads[str(m) + str(n + 1)][1][d] + alfa*(get_minilink(junc,destin_junction[d])-get_minilink(str(m) + str(n + 1),destin_junction[d])))
                            dif_vir[2].append(vir_onroads[junc][2][d] - vir_onroads[str(m - 1) + str(n)][2][d] + alfa*(get_minilink(junc,destin_junction[d])-get_minilink(str(m - 1) + str(n),destin_junction[d])))
                            dif_vir[3].append(vir_onroads[junc][3][d] - vir_onroads[str(m) + str(n - 1)][3][d] + alfa*(get_minilink(junc,destin_junction[d])-get_minilink(str(m) + str(n - 1),destin_junction[d])))

                        # 2.determine max pressure difference of each destination
                        dif_max0 = max(dif_vir[0])  # four actions of a junction
                        dif_max1 = max(dif_vir[1])
                        dif_max2 = max(dif_vir[2])
                        dif_max3 = max(dif_vir[3])

                        # 3.determine max destination with max difference
                        dif_list = [dif_max0, dif_max1, dif_max2, dif_max3]
                        max_destin = dif_list.index(max(dif_max0, dif_max1, dif_max2, dif_max3))  # max action
                        max_d = dif_vir[max_destin].index(
                            max(dif_vir[max_destin]))  # return the number of max destin

                        f_a0 = vir_onroads[junc][0][max_d]
                        f_a1 = vir_onroads[junc][1][max_d]
                        f_a2 = vir_onroads[junc][2][max_d]
                        f_a3 = vir_onroads[junc][3][max_d]

                        f_b0 = vir_onroads[str(m + 1) + str(n)][0][max_d]
                        f_b1 = vir_onroads[str(m) + str(n + 1)][1][max_d]
                        f_b2 = vir_onroads[str(m - 1) + str(n)][2][max_d]
                        f_b3 = vir_onroads[str(m) + str(n - 1)][3][max_d]

                        # 4.choose max pressure release phase
                        pressure_phasea = (f_a3 - f_b3) * u + (f_a3 - f_b0) * u + (f_a1 - f_b1) * u + \
                                          (f_a1 - f_b2) * u
                        pressure_phaseb = (f_a0 - f_b0) * u + (f_a0 - f_b1) * u + \
                                          (f_a2 - f_b2) * u + (f_a2 - f_b3) * u
                        pressure_phasec = (f_a1 - f_b0) * u + (f_a3 - f_b2) * u
                        pressure_phased = (f_a2 - f_b1) * u + (f_a0 - f_b3) * u

                        # determine phase:0 1 2 3
                        phase_list = [pressure_phaseb, pressure_phased, pressure_phasea, pressure_phasec]
                        for pha in phase_list:
                            if pha < 0:
                                pha = 0
                        traVeh = max(phase_list)
                        max_index = phase_list.index(max(phase_list))
                        if traVeh == 0:
                            action[junc] = random.randint(0, 3)
                        else:
                            action[junc] = max_index

                        if action[junc] == previous_action[junc]:  # action not changed
                            transition_phase[junc] = 0  # not a transition phase
                            traci.trafficlights.setPhase("N_" + junc, junction_phase[junc][action[junc]])
                            # print('set new phase to: ',phase[action])
                            timer_len[junc] = action_duration
                        else:  # action changed
                            transition_phase[junc] = 1  # it is a transition phase
                            timer_len[junc] = transition_duration
                            traci.trafficlights.setPhase("N_" + junc,
                                                         junction_phase[junc][previous_action[junc]] + 1)
                            # print('transition phase: ',phase[previous_action]+1)




                        # determine route
                        # 1. calculate virtual trans for every direction
                        trans_vir_r0 = dict.fromkeys(destination)
                        trans_vir_r1 = dict.fromkeys(destination)
                        trans_vir_r2 = dict.fromkeys(destination)
                        trans_vir_r3 = dict.fromkeys(destination)
                        for k in destination:  # right0, ahead1 and left2 for three direction
                            trans_vir_r0[k] = [0, 0, 0]
                            trans_vir_r1[k] = [0, 0, 0]
                            trans_vir_r2[k] = [0, 0, 0]
                            trans_vir_r3[k] = [0, 0, 0]
                        beta = 0.1
                        for k in destination:
                            for turn in xrange(3):
                                trans_vir_r0[k][turn] = (1 - beta) * pre_exTrans_r0[k][turn]
                                trans_vir_r1[k][turn] = (1 - beta) * pre_exTrans_r1[k][turn]
                                trans_vir_r2[k][turn] = (1 - beta) * pre_exTrans_r2[k][turn]
                                trans_vir_r3[k][turn] = (1 - beta) * pre_exTrans_r3[k][turn]
                            if k == destination[max_d]:
                                if action[junc] == 0:
                                    trans_vir_r1[k][0] += beta * u
                                    trans_vir_r1[k][1] += beta * u
                                    trans_vir_r3[k][0] += beta * u
                                    trans_vir_r3[k][1] += beta * u
                                if action[junc] == 1:
                                    trans_vir_r1[k][2] += beta * u
                                    trans_vir_r3[k][2] += beta * u
                                if action[junc] == 2:
                                    trans_vir_r0[k][0] += beta * u
                                    trans_vir_r0[k][1] += beta * u
                                    trans_vir_r2[k][0] += beta * u
                                    trans_vir_r2[k][1] += beta * u
                                if action[junc] == 3:
                                    trans_vir_r0[k][2] += beta * u
                                    trans_vir_r1[k][2] += beta * u

                        # renew pre_exTrans:sita(t-1)
                        for k in destination:
                            for turn in xrange(3):
                                pre_exTrans_r0[k][turn] = trans_vir_r0[k][turn]
                                pre_exTrans_r1[k][turn] = trans_vir_r1[k][turn]
                                pre_exTrans_r2[k][turn] = trans_vir_r2[k][turn]
                                pre_exTrans_r3[k][turn] = trans_vir_r3[k][turn]

                        # calculate the probability and renew route
                        # 1. get vehicle information of four roads
                        edgelist = [str(m - 1) + str(n) + "_" + junc, str(m) + str(n - 1) + "_" + junc,
                                    str(m + 1) + str(n) + "_" + junc, str(m) + str(n + 1) + "_" + junc]
                        veId = dict.fromkeys(edgelist)
                        veIdDes = dict.fromkeys(edgelist)
                        turnProb0 = dict.fromkeys(destination)
                        turnProb1 = dict.fromkeys(destination)
                        turnProb2 = dict.fromkeys(destination)
                        turnProb3 = dict.fromkeys(destination)
                        for k in destination:
                            turnProb0[k] = [0, 0, 0]
                            turnProb1[k] = [0, 0, 0]
                            turnProb2[k] = [0, 0, 0]
                            turnProb3[k] = [0, 0, 0]
                        sump0 = dict.fromkeys(destination, 0)
                        sump1 = dict.fromkeys(destination, 0)
                        sump2 = dict.fromkeys(destination, 0)
                        sump3 = dict.fromkeys(destination, 0)
                        for k in destination:
                            for x in xrange(3):
                                sump0[k] += trans_vir_r0[k][x]
                                sump1[k] += trans_vir_r1[k][x]
                                sump2[k] += trans_vir_r2[k][x]
                                sump3[k] += trans_vir_r3[k][x]
                        for k in destination:
                            for x in xrange(3):
                                turnProb0[k][x] = trans_vir_r0[k][x] / sump0[k]
                                turnProb1[k][x] = trans_vir_r1[k][x] / sump1[k]
                                turnProb2[k][x] = trans_vir_r2[k][x] / sump2[k]
                                turnProb3[k][x] = trans_vir_r3[k][x] / sump3[k]
                        for k in edgelist:
                            veId[k] = traci.edge.getLastStepVehicleIDs(k)
                            veIdDes[k] = dict.fromkeys(destination)
                            for des in destination:
                                veIdDes[k][des] = []
                            for id in veId[k]:
                                if veIdpre[junc][k].count(id) == 0:  # decide if need renew route
                                    dna = id[0:2]
                                    veIdDes[k][dna].append(id)
                            veIdpre[junc][k] = veId[k]


                        for des in destination:
                            # road0 of junction
                            if len(veIdDes[edgelist[0]][des]) != 0:
                                s = veIdDes[edgelist[0]][des]  # list not string
                                for vid in s:
                                    roupre = traci.vehicle.getRoute(vid)
                                    irou = len(roupre) - 1
                                    route = []
                                    route.append(roupre[irou])
                                    roupre = route
                                    destinV = vid[0:2]
                                    if destination.count(destinV) != 0:
                                        st_edge1 = roupre[len(roupre) - 1][3:5]
                                        stm = int(roupre[len(roupre) - 1][3])
                                        stn = int(roupre[len(roupre) - 1][4])
                                        p_right_l = turnProb0[des][0]/(turnProb0[des][0] + turnProb0[des][2])
                                        p_left_r = turnProb0[des][2]/(turnProb0[des][0] + turnProb0[des][2])
                                        p_ahead_r = turnProb0[des][1]/(turnProb0[des][0] + turnProb0[des][1])
                                        p_right_a = turnProb0[des][0]/(turnProb0[des][0] + turnProb0[des][1])
                                        p_ahead_l = turnProb0[des][1]/(turnProb0[des][1] + turnProb0[des][2])
                                        p_left_a = turnProb0[des][2] / (turnProb0[des][1] + turnProb0[des][2])
                                        rName = str(stm+1) + str(stn)
                                        if destin_junction.count(rName) != 0 and \
                                                        destin_junction.index(rName) == destination.index(destinV):
                                            routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 6 and stn != 6 and stn != 1:  # east boundary
                                            if random.uniform(0, 1) < p_right_l:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 6 and stn == 6:  # north-east conner
                                            routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 6 and stn == 1:   # south-east conner
                                            routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stn == 1:   # south boundary
                                            if random.uniform(0, 1) < p_ahead_l:
                                                routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stn == 6:   # north boundary
                                            if random.uniform(0, 1) < p_ahead_r:
                                                routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)

                                        elif random.uniform(0, 1) < turnProb0[des][0]:
                                            routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif random.uniform(0, 1) < turnProb0[des][0] + turnProb0[des][1]:
                                            routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        else:
                                            routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                            # road1 of junction
                            if len(veIdDes[edgelist[1]][des]) != 0:
                                s = veIdDes[edgelist[1]][des]  # list not string
                                for vid in s:
                                    roupre = traci.vehicle.getRoute(vid)
                                    irou = len(roupre) - 1
                                    route = []
                                    route.append(roupre[irou])
                                    roupre = route
                                    destinV = vid[0:2]
                                    if destination.count(destinV) != 0:
                                        st_edge1 = roupre[len(roupre) - 1][3:5]
                                        stm = int(roupre[len(roupre) - 1][3])
                                        stn = int(roupre[len(roupre) - 1][4])

                                        p_right_l = turnProb0[des][0] / (turnProb0[des][0] + turnProb0[des][2])
                                        p_left_r = turnProb0[des][2] / (turnProb0[des][0] + turnProb0[des][2])
                                        p_ahead_r = turnProb0[des][1] / (turnProb0[des][0] + turnProb0[des][1])
                                        p_right_a = turnProb0[des][0] / (turnProb0[des][0] + turnProb0[des][1])
                                        p_ahead_l = turnProb0[des][1] / (turnProb0[des][1] + turnProb0[des][2])
                                        p_left_a = turnProb0[des][2] / (turnProb0[des][1] + turnProb0[des][2])
                                        rName = str(stm) + str(stn+1)
                                        if destin_junction.count(rName) != 0 and \
                                                        destin_junction.index(rName) == destination.index(destinV):
                                            routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stn == 6 and stm != 6 and stm != 1:  # north boundary
                                            if random.uniform(0, 1) < p_right_l:
                                                routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm - 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 6 and stn == 6:  # north-east conner
                                            routemp = st_edge1 + "_" + str(stm-1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 1 and stn == 6:  # north-west conner
                                            routemp = st_edge1 + "_" + str(stm+1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 6:  # east boundary
                                            if random.uniform(0, 1) < p_ahead_l:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn+1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm-1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 1:  # west boundary
                                            if random.uniform(0, 1) < p_right_a:
                                                routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)

                                        elif random.uniform(0, 1) < turnProb0[des][0]:
                                            routemp = st_edge1 + "_" + str(stm+1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif random.uniform(0, 1) < turnProb0[des][0] + turnProb0[des][1]:
                                            routemp = st_edge1 + "_" + str(stm) + str(stn+1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        else:
                                            routemp = st_edge1 + "_" + str(stm-1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)


                            # road2 of junction
                            if len(veIdDes[edgelist[2]][des]) != 0:
                                s = veIdDes[edgelist[2]][des]  # list not string
                                for vid in s:
                                    if vid == "E3_0":
                                        traci.vehicle.setColor(vid, (255, 0, 0, 0))
                                    roupre = traci.vehicle.getRoute(vid)
                                    irou = len(roupre) - 1
                                    route = []
                                    route.append(roupre[irou])
                                    roupre = route
                                    destinV = vid[0:2]
                                    if destination.count(destinV) != 0:
                                        st_edge1 = roupre[len(roupre) - 1][3:5]
                                        stm = int(roupre[len(roupre) - 1][3])
                                        stn = int(roupre[len(roupre) - 1][4])
                                        p_right_l = turnProb0[des][0] / (turnProb0[des][0] + turnProb0[des][2])
                                        p_left_r = turnProb0[des][2] / (turnProb0[des][0] + turnProb0[des][2])
                                        p_ahead_r = turnProb0[des][1] / (turnProb0[des][0] + turnProb0[des][1])
                                        p_right_a = turnProb0[des][0] / (turnProb0[des][0] + turnProb0[des][1])
                                        p_ahead_l = turnProb0[des][1] / (turnProb0[des][1] + turnProb0[des][2])
                                        p_left_a = turnProb0[des][2] / (turnProb0[des][1] + turnProb0[des][2])

                                        rName = str(stm-1) + str(stn)
                                        if destin_junction.count(rName)!=0 and \
                                                        destin_junction.index(rName) == destination.index(destinV):
                                            routemp = st_edge1 + "_" + str(stm - 1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 1 and stn != 1 and stn != 6:  # west boundary
                                            if random.uniform(0, 1) < p_right_l:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 1 and stn == 1:  # north-east conner
                                            routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 1 and stn == 6:  # south-east conner
                                            routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stn == 6:  # north boundary
                                            if random.uniform(0, 1) < p_ahead_l:
                                                routemp = st_edge1 + "_" + str(stm - 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stn == 1:  # south boundary
                                            if random.uniform(0, 1) < p_ahead_r:
                                                routemp = st_edge1 + "_" + str(stm - 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)

                                        elif random.uniform(0, 1) < turnProb0[des][0]:
                                            routemp = st_edge1 + "_" + str(stm) + str(stn + 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif random.uniform(0, 1) < turnProb0[des][0] + turnProb0[des][1]:
                                            routemp = st_edge1 + "_" + str(stm - 1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        else:
                                            routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)

                            # road3 of junction
                            if len(veIdDes[edgelist[3]][des]) != 0:
                                s = veIdDes[edgelist[3]][des]  # list not string
                                for vid in s:
                                    if vid == "E3_0":
                                        traci.vehicle.setColor(vid, (255, 0, 0, 0))
                                    roupre = traci.vehicle.getRoute(vid)
                                    irou = len(roupre) - 1
                                    route = []
                                    route.append(roupre[irou])
                                    roupre = route
                                    destinV = vid[0:2]
                                    if destination.count(destinV) != 0:
                                        st_edge1 = roupre[len(roupre) - 1][3:5]
                                        stm = int(roupre[len(roupre) - 1][3])
                                        stn = int(roupre[len(roupre) - 1][4])

                                        p_right_l = turnProb0[des][0] / (turnProb0[des][0] + turnProb0[des][2])
                                        p_left_r = turnProb0[des][2] / (turnProb0[des][0] + turnProb0[des][2])
                                        p_ahead_r = turnProb0[des][1] / (turnProb0[des][0] + turnProb0[des][1])
                                        p_right_a = turnProb0[des][0] / (turnProb0[des][0] + turnProb0[des][1])
                                        p_ahead_l = turnProb0[des][1] / (turnProb0[des][1] + turnProb0[des][2])
                                        p_left_a = turnProb0[des][2] / (turnProb0[des][1] + turnProb0[des][2])

                                        rName = str(stm) + str(stn-1)
                                        if destin_junction.count(rName) and\
                                                        destin_junction.index(rName) == destination.index(destinV):
                                            routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stn == 1 and stm != 6 and stm != 1:  # south boundary
                                            if random.uniform(0, 1) < p_right_l:
                                                routemp = st_edge1 + "_" + str(stm - 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 1 and stn == 1:  # south-west conner
                                            routemp = st_edge1 + "_" + str(stm+1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 6 and stn == 1:  # south-east conner
                                            routemp = st_edge1 + "_" + str(stm-1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 1:  # west boundary
                                            if random.uniform(0, 1) < p_ahead_l:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm + 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                        elif stm == 6:  # east boundary
                                            if random.uniform(0, 1) < p_ahead_r:
                                                routemp = st_edge1 + "_" + str(stm) + str(stn - 1)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)
                                            else:
                                                routemp = st_edge1 + "_" + str(stm - 1) + str(stn)
                                                roupre.append(routemp)
                                                traci.vehicle.setRoute(vid, roupre)

                                        elif random.uniform(0, 1) < turnProb0[des][0]:
                                            routemp = st_edge1 + "_" + str(stm-1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        elif random.uniform(0, 1) < turnProb0[des][0] + turnProb0[des][1]:
                                            routemp = st_edge1 + "_" + str(stm) + str(stn-1)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)
                                        else:
                                            routemp = st_edge1 + "_" + str(stm+1) + str(stn)
                                            roupre.append(routemp)
                                            traci.vehicle.setRoute(vid, roupre)

            # excecute simulation
            traci.simulationStep()
            step += 1  # important note: step increases only if sim is executed
            for junction in edge_name:
                timer[junction] += 1

            # timer expires, decide if we observe rewards or change action
            for junction in trafficLight_edge:
                if timer[junction] == timer_len[junction]:
                    if transition_phase[junction] == 1:
                        transition_phase[junction] = 0
                        timer[junction] = 0
                        traci.trafficlights.setPhase("N_" + junction, junction_phase[junction][action[junction]])
                        timer_len[junction] = action_duration
                    else:
                        timer[junction] = 0  # reset timer
                        previous_action[junction] = action[junction]
                        select_action[junction] = 1

        traci.close()
        sys.stdout.flush()
        t1 = time.time()
        print('time consumed: ', t1 - t0)
        sum_delay = 0
        num_delay = 0
        # f_staytime.write('test vehicle total num:' + str(num_delay) + '\n')
        # f_staytime.write('average:' + str(sum_delay/num_delay) + '\n')

f_staytime.close()
