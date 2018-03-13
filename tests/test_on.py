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

def test_add_random_work():

    agent_id = on.add_random_agent()
    work_id = on.add_random_work(agent_id)
    print("added random work", work_id)
    assert work_id in g.agent(agent_id).works(work_id).properties(ns.KEY_WORK_ID).value().toList()
    assert g.agent(agent_id).works().has(ns.KEY_WORK_ID, work_id).work_items(ns.EDGE_DEMANDS).count().next() == 1
    assert g.agent(agent_id).works().has(ns.KEY_WORK_ID, work_id).work_items(ns.EDGE_OFFERS).count().next() == 1

def test_add_chain():
    """Test chain"""
    chained_works = on.add_chain(4)
    print('created chain of works %s' % chained_works)

    demand_first = g.work(chained_works[0]).work_items(ns.EDGE_DEMANDS).properties(ns.KEY_ITEM_VALUE).value().next()
    offer_last = g.work(chained_works[-1]).work_items(ns.EDGE_OFFERS).properties(ns.KEY_ITEM_VALUE).value().next()
    assert demand_first == offer_last
    for i in range(len(chained_works)-1):
        offer = g.work(chained_works[i]).work_items(ns.EDGE_OFFERS).properties(ns.KEY_ITEM_VALUE).value().next()
        print('retrieved offer %s from work %s' %(offer, chained_works[i]))
        demand = g.work(chained_works[i+1]).work_items(ns.EDGE_DEMANDS).properties(ns.KEY_ITEM_VALUE).value().next()
        print('retrieved demand %s from work %s' % (demand, chained_works[i+1]))
        assert offer == demand

