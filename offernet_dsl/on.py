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
from offernet_dsl.ns import *
import time
import random


client = Client('ws://localhost:8182/gremlin', 'g')
rc = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
on = Graph().traversal(OfferNetTraversalSource).withRemote(rc)

def init():
    make_keys_msg = f"""graph.tx().rollback()
                    mgmt = graph.openManagement()
                    
                    // make propertyKeys                    
                    mgmt.makePropertyKey('{VERTEX_TYPE}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{KEY_AGENT_ID}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_OWNS}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_KNOWS}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_SIMILAR}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_OFFERS}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{EDGE_DEMANDS}').dataType(String.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.makePropertyKey('{KEY_ITEM_VALUE}').dataType(Array.class).cardinality(Cardinality.SINGLE).make()
                    mgmt.commit()"""

    schema_msg = f"""graph.tx().rollback()
                    mgmt = graph.openManagement()
                    
                    vertexType = mgmt.getPropertyKey('{VERTEX_TYPE}')
                    mgmt.buildIndex('byVertexTypeComposite', Vertex.class).addKey(vertexType).buildCompositeIndex()
                    
                    keyAgentId = mgmt.getPropertyKey('{KEY_AGENT_ID}')
                    mgmt.buildIndex('byKeyAgentIdComposite', Vertex.class).addKey(keyAgentId).buildCompositeIndex()
                    
                    edgeOwns = mgmt.getPropertyKey('{EDGE_OWNS}')
                    mgmt.buildIndex('byEdgeOwnsComposite', Edge.class).addKey(edgeOwns).buildCompositeIndex()
                    
                    edgeKnows = mgmt.getPropertyKey('{EDGE_KNOWS}')
                    mgmt.buildIndex('byEdgeKnowsComposite', Edge.class).addKey(edgeKnows).buildCompositeIndex()
                    
                    edgeSimilar = mgmt.getPropertyKey('{EDGE_SIMILAR}')
                    mgmt.buildIndex('byEdgeSimilarComposite', Edge.class).addKey(edgeSimilar).buildCompositeIndex()
                    
                    edgeOffers = mgmt.getPropertyKey('{EDGE_OFFERS}')
                    mgmt.buildIndex('byEdgeOffersComposite', Edge.class).addKey(edgeOffers).buildCompositeIndex()
                    
                    edgeDemands = mgmt.getPropertyKey('{EDGE_DEMANDS}')
                    mgmt.buildIndex('byEdgeDemandsComposite', Edge.class).addKey(edgeDemands).buildCompositeIndex()

                    keyItemValue = mgmt.getPropertyKey('{KEY_ITEM_VALUE}')
                    mgmt.buildIndex('byKeyItemValueComposite', Vertex.class).addKey(keyItemValue).buildCompositeIndex()
                    
                    mgmt.commit()
                    
                    mgmt.awaitGraphIndexStatus(graph, 'byVertexTypeComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byKeyAgentIdComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeOwnsComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeKnowsComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeSimilarComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeOffersComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byEdgeDemandsComposite').call()
                    mgmt.awaitGraphIndexStatus(graph, 'byKeyItemValueComposite').call()
                    
                    mgmt = graph.openManagement()
                    mgmt.updateIndex(mgmt.getGraphIndex("byVertexTypeComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byKeyAgentIdComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeOwnsComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeKnowsComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeSimilarComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeOffersComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byEdgeDemandsComposite"), SchemaAction.REINDEX).get()
                    mgmt.updateIndex(mgmt.getGraphIndex("byKeyItemValueComposite"), SchemaAction.REINDEX).get()
                    mgmt.commit()"""
    client.submit(make_keys_msg)
    time.sleep(2)
    client.submit(schema_msg)

    if len(on.V().has('type', 'GlobalOfferNetProperties').toList()) is 0:
        on.addV('GlobalOfferNetProperties').property('type', 'GlobalOfferNetProperties').next()

def add_random_agent():
    """
    Add an agent to the network and connect to another agent randomly -- returns newly added agents id
    Returns agent id
    """

    new_agent_id = on.create_agent().properties(KEY_AGENT_ID).value().next()
    random_agent = get_random_agent()

    if random_agent is None:
        random_agent = on.create_agent()

    new_agent = on.agent(new_agent_id)
    random_agent.knows(new_agent).next()
    return new_agent_id


def get_random_agent():
    """
    Get random agent from the network
    Returns: agent vertex
    """

    agents = on.V().has('type', 'agent').properties(KEY_AGENT_ID).value().toList()
    random_agent = on.agent(random.choice(agents))

    return random_agent

def add_random_work(agent_id):
    """
    Add random work to an agent (i.e. with randomly generated demand and offer)
    Returns work id
    """

    work = on.create_work()
    on.agent(agent_id).owns_work(work).next()
    work_id = on.agent(agent_id).works().properties(KEY_WORK_ID).value().next()
    item1 = on.create_item()
    item2 = on.create_item()
    demand = on.agent(agent_id).works(work_id).demands(item1).next()
    print("added random demand: ", demand)
    offer = on.agent(agent_id).works(work_id).offers(item2).next()
    print("added random offer: ", offer)
    return work_id

