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