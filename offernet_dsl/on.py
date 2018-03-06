#
# offernet_dsl/on.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from gremlin_python.driver.client import Client
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


VERTEX_AGENT='agent'
VERTEX_WORK='work'
VERTEX_ITEM='item'

EDGE_OWNS='owns'
EDGE_SIMILAR='similar'
EDGE_OFFERS='offers'
EDGE_DEMANDS='demands'

KEY_AGENT_ID='agentId'

def init():
    client = Client('ws://localhost:8182/gremlin', 'g')
    rc = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = Graph().traversal().withRemote(rc)

    if len(g.V().hasLabel('GlobalOfferNetProperties').toList()) is 0:
        g.addV('GlobalOfferNetProperties').next()

    schema_msg = """mgmt = graph.openManagement()
                    string_prop = mgmt.makePropertyKey('agentId').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.commit()"""
    client.submit(schema_msg)
