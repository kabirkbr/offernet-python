#
# tests/test_janusgraph.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import pytest
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import random

log = logging.getLogger(__name__)

graph = Graph()
g = graph.traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin', 'g'))

def test_connection():
    identity = random.randint(1, 1001)

    #adding a vertex
    v = g.addV('vertex').property('idnt', identity).property('name', 'vertexName').id().toList()[0]

    #checking if vertex exists
    vertexIdentity = g.V(v).idnt.toList()[0]
    assert identity == vertexIdentity

    #cleaning graph
    g.V().drop().iterate()
