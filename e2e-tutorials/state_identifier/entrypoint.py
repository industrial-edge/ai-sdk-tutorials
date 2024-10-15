# SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.
#
# SPDX-License-Identifier: MIT

import json
import sys
from pathlib import Path

from log_module import LogModule
logger = LogModule()

sys.path.insert(0, str(Path('./src').resolve()))
from si import inference  # should adapt to your code

logger.info("entrypoint imported")


def process_input(data: dict):

    return inference.process_data(data)


def update_parameters(params: dict):

    inference.update_parameters(params)
