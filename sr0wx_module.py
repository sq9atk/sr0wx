#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2014 Michal Sadowski (sq6jnx at hamradio dot pl)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import warnings


class SR0WXModule(object):
    """Base class for SR0WX modules."""
    def __init__(self):
        pass

    def getData(self):
        """Deprecated method. Runs `get_data()`."""
        msg = "Use if getData() is deprecated, use get_data() instead"
        warnings.warn(msg)
        return self.get_data()

    def get_data(self):
        """Returns message to be played back by core of sr0wx.py. Not
implemented here.

Modules are expected to return a `dict` with the following keys:
    - `message` -- message text, filled template, etc (currently list of
    samples)
    - `need_ctcss` -- hint for core module whether or not to playback CTCSS tone
"""
        msg = "This method should be implemented in child class"
        raise NotImplementedError(msg)
