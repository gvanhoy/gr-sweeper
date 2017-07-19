#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import pmt

class sweeper(gr.sync_block):
    """
    docstring for block sweeper
    """
    def __init__(self, initial_freq=630e6, step=6e6, max_freq=862e6):
        gr.sync_block.__init__(self,
            name="sweeper",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('clock'))
        self.set_msg_handler(pmt.intern('clock'), self.handler)
        self.message_port_register_out(pmt.intern('msg_out'))
        self.freq = initial_freq
        self.reset_freq = initial_freq
        self.step = step
        self.max_freq = max_freq


    def handler(self, pdu):
        self.message_port_pub(pmt.intern('msg_out'), pmt.cons(pmt.intern('freq'),pmt.to_pmt(self.freq)))

        if self.freq < self.max_freq:
            self.freq += self.step
        else:
            self.freq = self.reset_freq

