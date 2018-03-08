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
from offernet_dsl.on import *
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

    def all_works(self):
        """Retrieves all works of an agent"""
        traversal = self.out(EDGE_OWNS)
        return traversal

    def demands(self, item):
        """Adds existing item to a work vertex as a demand"""
        traversal = self.addE(EDGE_DEMANDS).to(item)
        return traversal

    def offers(self, item):
        """Adds existing item to a work vertex as an offer"""

        traversal = self.addE(EDGE_OFFERS).to(item)
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

