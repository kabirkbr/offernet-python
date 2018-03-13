#
# offernet_dsl/dsl.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from gremlin_python.process.traversal import (Bytecode, P, Scope, Order, Column, T)
from gremlin_python.process.graph_traversal import (GraphTraversalSource, GraphTraversal)
from gremlin_python.process.graph_traversal import __ as AnonymousTraversal
import uuid
from offernet_dsl.ns import *
from offernet_dsl.utils import *

V = AnonymousTraversal.V
addV = AnonymousTraversal.addV
outE = AnonymousTraversal.outE
outV = AnonymousTraversal.outV
count = AnonymousTraversal.count
unfold = AnonymousTraversal.unfold

gt = P.gt
lt = P.lt
between = P.between
within = P.within
local = Scope.local
decr = Order.decr
values = Column.values
keys = Column.keys

class OfferNetTraversal(GraphTraversal):
    """The OfferNet Traversal class which exposes the available steps of the DSL."""

    def knows(self, to_agent):
        """Tells that this agent knows another agent"""

        traversal = self.addE(EDGE_KNOWS).to(to_agent)
        return traversal

    def owns_work(self, work):
        """This agent owns work"""
        traversal = self.addE(EDGE_OWNS).to(work)
        return traversal

    def works(self, work_id=''):
        """Retrieves all works of an agent or a specific work by Id, if id is given"""

        traversal = self
        if work_id == '':
            traversal = traversal.out(EDGE_OWNS)
        else:
            traversal = traversal.out(EDGE_OWNS).has(KEY_WORK_ID, work_id)

        return traversal

    def demands(self, item):
        """Adds existing item to a work vertex as a demand"""
        traversal = self.addE(EDGE_DEMANDS).to(item)
        return traversal

    def offers(self, item):
        """Adds existing item to a work vertex as an offer"""
        traversal = self.addE(EDGE_OFFERS).to(item)
        return traversal

    def agent_items(self, which='all'):
        """Gets items of the works of an agent"""

        traversal = self.outE(EDGE_OWNS).inV().has(VERTEX_TYPE, VERTEX_WORK)

        if which == 'all':
            traversal = traversal.outE().inV().has(VERTEX_TYPE, VERTEX_ITEM)
        elif which == 'demands':
            traversal = traversal.outE(EDGE_DEMANDS).inV().has(VERTEX_TYPE, VERTEX_ITEM)
        elif which == 'offers':
            traversal = traversal.outE(EDGE_OFFERS).inV().has(VERTEX_TYPE, VERTEX_ITEM)

        return traversal

    def work_items(self, which='all'):
        """Gets items of a work"""
        traversal = self

        if which == 'all':
            traversal = traversal.outE().inV().has(VERTEX_TYPE, VERTEX_ITEM)
        elif which == ns.EDGE_DEMANDS:
            traversal = traversal.outE(ns.EDGE_DEMANDS).inV().has(VERTEX_TYPE, VERTEX_ITEM)
        elif which == ns.EDGE_OFFERS:
            traversal = traversal.outE(ns.EDGE_OFFERS).inV().has(VERTEX_TYPE, VERTEX_ITEM)

        return traversal

class __(AnonymousTraversal):
    """Spawns anonymous OfferNetTraversal instances for the DSL."""

    graph_traversal = OfferNetTraversal

    @classmethod
    def agent(cls, *args):
        return cls.graph_traversal(None, None, Bytecode().agent(*args))

class OfferNetTraversalSource(GraphTraversalSource):
    """
    The OfferNet DSL TraversalSource which will provide the start steps for DSL-based traversals.
    This TraversalSource spawns OfferNetTraversal instances.
    """

    def __init__(self, *args, **kwargs):
        super(OfferNetTraversalSource, self).__init__(*args, **kwargs)
        self.graph_traversal = OfferNetTraversal  # tells the "source" the type of Traversal to spawn

    def create_agent(self):
        """Creates a new agent and returns it"""

        traversal = self.get_graph_traversal().addV(VERTEX_AGENT).property(VERTEX_TYPE, VERTEX_AGENT).property(KEY_AGENT_ID, str(uuid.uuid4()))
        return traversal

    def agent(self, agent_id):
        """Gets an agent by the id (not sure this is needed in decentralized system) !!!"""
        traversal = self.get_graph_traversal().V().has(KEY_AGENT_ID, agent_id)
        return traversal

    def work(self, work_id):
        """Gets work directly from the graph -- only for testing purposes"""
        traversal = self.get_graph_traversal().V().has(VERTEX_TYPE, VERTEX_WORK).has(KEY_WORK_ID, work_id)
        return traversal

    def create_work(self):
        """Creates new work and returns it"""
        traversal = self.get_graph_traversal().addV(VERTEX_WORK).property(VERTEX_TYPE, VERTEX_WORK).property(
            KEY_WORK_ID, str(uuid.uuid4()))
        return traversal

    def create_item(self, *value):
        """Creates new item and returns it"""
        if len(value) == 0:
            vector = binary_array(ITEM_VECTOR_LENGTH)
        else:
            vector = value[0]

        traversal = self.get_graph_traversal().addV(VERTEX_ITEM).property(VERTEX_TYPE, VERTEX_ITEM).property(KEY_ITEM_ID, str(uuid.uuid4())).property(KEY_ITEM_VALUE, vector)

        return traversal

