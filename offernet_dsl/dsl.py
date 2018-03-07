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

    def knows_agent(self, to_agent):
        self.addE('knows').to(to_agent)

    # finished here...

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
