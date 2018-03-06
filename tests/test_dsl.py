#
# tests/test_dsl.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import pytest
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from offernet_dsl.dsl import OfferNetTraversalSource
from offernet_dsl.dsl import *
from offernet_dsl.on import *

log = logging.getLogger(__name__)

offernet = Graph().traversal(OfferNetTraversalSource).withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin', 'g'))

def test_new_agent():
    a1 = offernet.new_agent().label().next()
    print('created agent: ', a1)
    assert a1 == VERTEX_AGENT

def test_agent():
    a1 = offernet.new_agent().properties(KEY_AGENT_ID).value().next()
    print('created agent: ', a1)
    a2 = offernet.agent(a1).properties(KEY_AGENT_ID).value().next()
    assert a1 == a2
