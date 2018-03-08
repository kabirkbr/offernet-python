#
# offernet_dsl/utils.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from numpy.random import randint
import json

def binary_array(length):
    array = randint(2, size=length).tolist()
    json_string = json.dumps(array)
    return json_string



