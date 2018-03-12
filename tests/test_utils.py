#
# tests/test_utils.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from offernet_dsl.utils import *
from offernet_dsl.ns import *
import json

def test_binary_array(length = ns.ITEM_VECTOR_LENGTH):
    ba = binary_array(length)
    print('generated random binary array: ', ba)
    assert len(json.loads(ba)) == length

def test_generate_chain():
    chain = generate_chain(5)
    print('generated chain: ', chain)
    assert len(chain) == 5

def test_add_chain():
    assert 1 == 0 # write test
