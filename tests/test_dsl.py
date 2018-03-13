#
# tests/test_dsl.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import pytest
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from offernet_dsl.dsl import *
from offernet_dsl.ns import *
from offernet_dsl.utils import *

log = logging.getLogger(__name__)

g = Graph().traversal(OfferNetTraversalSource).withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin', 'g'))

#tests for OfferNetTraversal
def test_knows():
    """Tests adding an already created agent as known to another"""
    a1 = g.create_agent().properties(KEY_AGENT_ID).value().next()
    print('agent1: ',a1)
    a2 = g.create_agent().properties(KEY_AGENT_ID).value().next()
    print('agent2: ', a2)
    edge = g.agent(a1).knows(g.agent(a2)).next()
    print('edge: ', edge)
    assert edge is not None

# tests for OfferNetTraversalSource
def test_create_agent():
    a1 = g.create_agent().properties(VERTEX_TYPE).value().next()
    print('created agent: ', a1)
    assert a1 == VERTEX_AGENT

def test_agent():
    a1 = g.create_agent().properties(KEY_AGENT_ID).value().next()
    print('created agent: ', a1)
    a2 = g.agent(a1).properties(KEY_AGENT_ID).value().next()
    assert a1 == a2

def test_work():
    work_id = g.create_work().properties(KEY_WORK_ID).value().next()
    print('created work: ', work_id)
    assert g.work(work_id).properties(VERTEX_TYPE).value().next() == VERTEX_WORK

def test_create_work():
    w1 = g.create_work().properties(VERTEX_TYPE).value().next()
    print('created work: ', w1)
    assert w1 == VERTEX_WORK

def test_create_random_item():
    i1 = g.create_item().properties(VERTEX_TYPE).value().next()
    print('created work: ', i1)
    assert i1 == VERTEX_ITEM

def test_create_nonrandom_item():
    value = binary_array(ITEM_VECTOR_LENGTH)
    i1 = g.create_item(value).properties(VERTEX_TYPE).value().next()
    print('created work: ', i1)
    assert i1 == VERTEX_ITEM

def test_owns_work():
    a1 = g.create_agent()
    w1 = g.create_work()
    ownsEdge = a1.owns_work(w1)
    print('Created owns edge: ', ownsEdge)
    assert ownsEdge.label().next() == EDGE_OWNS

def test_all_works():
    a1 = g.create_agent().properties(KEY_AGENT_ID).value().next()
    w1 = g.create_work()
    w2 = g.create_work()
    g.agent(a1).owns_work(w1).next()
    g.agent(a1).owns_work(w2).next()

    works = g.agent(a1).works().properties(VERTEX_TYPE).value().toList()
    assert len(works) == 2
    for work in works:
        assert work == VERTEX_WORK

def test_demands():
    w1 = g.create_work()
    i1 = g.create_item()
    demandsEdge = w1.demands(i1)
    print('Created demands edge: ', demandsEdge)
    assert demandsEdge.label().next() == EDGE_DEMANDS

def test_offers():
    w1 = g.create_work()
    i1 = g.create_item()
    offersEdge = w1.offers(i1)
    print('Created offers edge: ', offersEdge)
    assert offersEdge.label().next() == EDGE_OFFERS

def test_agent_items():
    a1id = g.create_agent().properties(KEY_AGENT_ID).value().next()
    w1 = g.create_work()
    w2 = g.create_work()
    g.agent(a1id).owns_work(w1).next()
    g.agent(a1id).owns_work(w2).next()

    g.agent(a1id).works().demands(g.create_item()).next()
    g.agent(a1id).works().offers(g.create_item()).next()

    print('query', g.agent(a1id).agent_items().next())

    assert g.agent(a1id).agent_items().count().next() == 4
    assert g.agent(a1id).agent_items('demands').count().next() == 2
    assert g.agent(a1id).agent_items('offers').count().next() == 2


def test_work_items():
    w1 = g.create_work()
    i1 = g.create_item()
    demandsEdge = w1.demands(i1)
    print('Created demands edge: ', demandsEdge)
    assert demandsEdge.label().next() == EDGE_DEMANDS
