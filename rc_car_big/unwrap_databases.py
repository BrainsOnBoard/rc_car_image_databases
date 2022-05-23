#!/usr/bin/env python3
from glob import glob
import os

import bob_robotics.navigation as bobnav

UNWRAP_SIZE = (360, 1440)

this_dir = os.path.dirname(__file__)
for path in glob(os.path.join(this_dir, '2021*')):
    bobnav.Database(path, warn_if_not_unwrapped=False).unwrap(UNWRAP_SIZE)
