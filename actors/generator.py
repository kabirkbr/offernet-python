#
# actors/generator.py - unit test for the app.
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
import offernet_dsl.utils as utils
import random

client = Client('ws://localhost:8182/gremlin', 'g')
rc = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
g = Graph().traversal(OfferNetTraversalSource).withRemote(rc)

def add_random_agent():
    """
    Add an agent to the network and connect to another agent randomly -- returns newly added actors id
    Returns agent id
    """

    new_agent_id = g.create_agent().properties(KEY_AGENT_ID).value().next()
    random_agent = get_random_agent()

    if random_agent is None:
        random_agent = g.create_agent()

    new_agent = g.agent(new_agent_id)
    random_agent.knows(new_agent).next()
    return new_agent_id


def get_random_agent():
    """
    Get random agent from the network
    Returns: agent vertex
    """

    agents = g.V().has('type', 'agent').properties(KEY_AGENT_ID).value().toList()
    random_agent = g.agent(random.choice(agents))

    return random_agent

def add_random_work(agent_id):
    """
    Add random work to an agent (i.e. with randomly generated demand and offer)
    Returns work id
    """

    work = g.create_work()
    g.agent(agent_id).owns_work(work).next()
    work_id = g.agent(agent_id).works().properties(KEY_WORK_ID).value().next()
    item1 = g.create_item()
    item2 = g.create_item()
    demand = g.agent(agent_id).works(work_id).demands(item1).next()
    print("added random demand: ", demand)
    offer = g.agent(agent_id).works(work_id).offers(item2).next()
    print("added random offer: ", offer)
    return work_id

def add_chain(length):
    """Adds a chain to the network so that"""
    chained_works = []
    chain = utils.generate_chain(length)
    for i in range(len(chain)-1):
        agent_id = get_random_agent().properties(ns.KEY_AGENT_ID).value().next()
        work_id = g.create_work().properties(ns.KEY_WORK_ID).value().next()
        g.agent(agent_id).owns_work(g.work(work_id)).next()
        item1 = g.create_item(chain[i])
        g.agent(agent_id).works(work_id).demands(item1).next()
        item2 = g.create_item(chain[i+1])
        g.agent(agent_id).works(work_id).offers(item2).next()
        chained_works.append(work_id)

    return chained_works

