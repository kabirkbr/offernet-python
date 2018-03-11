#
# tests/test_on.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import pytest
import offernet_dsl.on as on
import offernet_dsl.ns as ns
from offernet_dsl.dsl import OfferNetTraversalSource

from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
g = Graph().traversal(OfferNetTraversalSource).withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin', 'g'))

log = logging.getLogger(__name__)

@pytest.mark.first
def test_init():
    on.init()


def test_add_random_agent():

    agent_id = on.add_random_agent()
    assert g.agent(agent_id).properties(ns.VERTEX_TYPE).value().next() == ns.VERTEX_AGENT


def test_get_random_agent():
    agent = on.get_random_agent().properties(ns.VERTEX_TYPE).value().next()
    assert agent == ns.VERTEX_AGENT
