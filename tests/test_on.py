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


log = logging.getLogger(__name__)

@pytest.mark.first
def test_init():
    on.init()


def test_add_random_agent():

    agent = on.add_random_agent().properties(on.VERTEX_TYPE).value().next()
    assert agent == on.VERTEX_AGENT


def test_get_random_agent():
    agent = on.get_random_agent().properties(on.KEY_AGENT_ID).value().next()
    assert agent == on.VERTEX_AGENT
