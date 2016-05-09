#!/usr/bin/env python
import os
from onelove.worker import run
from config import DevConfig


project_root = os.path.dirname(os.path.abspath(__file__))
run(project_root, DevConfig)
