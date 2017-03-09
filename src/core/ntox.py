# -*- encoding: utf-8 -*-
"""
ntox.py
===================

(C) RedIP GmbH, 2016 <info@red-ip.de>
"""

import sys
import os

# Integration of the external libs
script_path = "../external/"
sys.path.append(os.path.abspath(script_path))
from src.modules.discovery.discover import Discover

# Start of the APP
discover = Discover("192.168.100.0", "29")
discover.start_discover()
