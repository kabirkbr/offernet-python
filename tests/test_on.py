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

