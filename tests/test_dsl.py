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

on = Graph().traversal(OfferNetTraversalSource).withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin', 'g'))

#tests for OfferNetTraversal
def test_knows_agent():


# tests for OfferNetTraversalSource
def test_create_agent():
    a1 = on.create_agent().properties(VERTEX_TYPE).value().next()
    print('created agent: ', a1)
    assert a1 == VERTEX_AGENT

def test_agent():
    a1 = on.create_agent().properties(KEY_AGENT_ID).value().next()
    print('created agent: ', a1)
    a2 = on.agent(a1).properties(KEY_AGENT_ID).value().next()
    assert a1 == a2

