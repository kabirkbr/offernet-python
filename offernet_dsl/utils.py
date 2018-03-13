#
# offernet_dsl/utils.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from numpy.random import randint
import json
import offernet_dsl.ns as ns

def binary_array(length):
    array = randint(2, size=length).tolist()
    json_string = json.dumps(array)
    return json_string

def generate_chain(length):
    chain = []
    for i in range(length):
        chain.append(binary_array(ns.ITEM_VECTOR_LENGTH))

    chain.append(chain[0])
    print("generated chain: ", chain)
    return chain

