#
# tests/test_utils.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from offernet_dsl.utils import binary_array
from offernet_dsl.on import *
import json

def test_binary_array(length = ITEM_VECTOR_LENGTH):
    ba = binary_array(length)
    print('generated random binary array: ', ba)
    assert len(json.loads(ba)) == length



