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
from offernet_dsl.dsl import *
import time

VERTEX_TYPE='type'
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
    on = Graph().traversal(OfferNetTraversalSource).withRemote(rc)

    make_keys_msg = f"""graph.tx().rollback()
                    mgmt = graph.openManagement()
                    
                    // make propertyKeys                    
                    mgmt.makePropertyKey('{VERTEX_TYPE}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{KEY_AGENT_ID}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_OWNS}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_SIMILAR}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_OFFERS}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_DEMANDS}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.commit()"""

    schema_msg = f"""graph.tx().rollback()
                    mgmt = graph.openManagement()
                    
                    vertexType = mgmt.getPropertyKey('{VERTEX_TYPE}')
                    mgmt.buildIndex('byVertexTypeComposite', Vertex.class).addKey(vertexType).buildCompositeIndex()
                    
                    keyAgentId = mgmt.getPropertyKey('{KEY_AGENT_ID}')
                    mgmt.buildIndex('byKeyAgentIdComposite', Vertex.class).addKey(keyAgentId).buildCompositeIndex()
                    
                    edgeOwns = mgmt.getPropertyKey('{EDGE_OWNS}')
                    mgmt.buildIndex('byEdgeOwnsComposite', Edge.class).addKey(edgeOwns).buildCompositeIndex()
                    
                    edgeSimilar = mgmt.getPropertyKey('{EDGE_SIMILAR}')
                    mgmt.buildIndex('byEdgeSimilarComposite', Edge.class).addKey(edgeSimilar).buildCompositeIndex()
                    
                    edgeOffers = mgmt.getPropertyKey('{EDGE_OFFERS}')
                    mgmt.buildIndex('byEdgeOffersComposite', Edge.class).addKey(edgeOffers).buildCompositeIndex()
                    
                    edgeDemands = mgmt.getPropertyKey('{EDGE_DEMANDS}')
                    mgmt.buildIndex('byEdgeDemandsComposite', Edge.class).addKey(edgeDemands).buildCompositeIndex()
                    
                    mgmt.commit()
                    
                    mgmt.awaitGraphIndexStatus(graph, 'byVertexTypeComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byKeyAgentIdComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeOwnsComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeSimilarComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeOffersComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeDemandsComposite').call()
                    
                    mgmt = graph.openManagement()
                    mgmt.updateIndex(mgmt.getGraphIndex("byVertexTypeComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byKeyAgentIdComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeOwnsComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeSimilarComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeOffersComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeDemandsComposite"), SchemaAction.REINDEX).get()
                    mgmt.commit()"""
    client.submit(make_keys_msg)
    time.sleep(2)
    client.submit(schema_msg)

    if len(on.V().has('type', 'GlobalOfferNetProperties').toList()) is 0:
        on.addV('GlobalOfferNetProperties').property('type', 'GlobalOfferNetProperties').next()
