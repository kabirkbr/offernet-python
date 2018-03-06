import datetime
from on import *
from gremlin_python.process.traversal import (Bytecode, P, Scope, Order, Column, T)
from gremlin_python.process.graph_traversal import (GraphTraversalSource, GraphTraversal)
from gremlin_python.process.graph_traversal import __ as AnonymousTraversal
from aenum import Enum

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

    def id(self):
        """Returns and id of an agent vertex"""
        return self.id().next()

    def knows_agent(self, agent_id):
        self.addEdge('knows', OfferNetTraversalSource.agent(agent_id))

    # finished here...

class __(AnonymousTraversal):
    """Spawns anonymous OfferNetTraversal instances for the DSL."""

    graph_traversal=OfferNetTraversal

    @classmethod
    def

class OfferNetTraversalSource(GraphTraversalSource):
    """
    The OfferNet DSL TraversalSource which will provide the start steps for DSL-based traversals.
    This TraversalSource spawns OfferNetTraversal instances.
    """

    def __init__(self, *args, **kwargs):
        super(OfferNetTraversalSource, self).__init__(*args, **kwargs)
        self.graph_traversal = OfferNetTraversal  # tells the "source" the type of Traversal to spawn

    def agent(self,agent_id):
        traversal = self.get_graph_traversal().V(agent_id)
        return traversal

