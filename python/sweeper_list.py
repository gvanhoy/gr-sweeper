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

class sweeper_list(gr.sync_block):
    """
    docstring for block sweeper_list
    """
    def __init__(self, freq_list=[]):
        gr.sync_block.__init__(self,
            name="sweeper_list",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('change_freq'))
        self.set_msg_handler(pmt.intern('change_freq'), self.handler)
        self.message_port_register_out(pmt.intern('freq_out')) 
        self.freq_list = freq_list
        self.freq_index = 0

    def handler(self):
        if self.freq_index >= len(self.freq_list):
            self.freq = self.freq_list[0]
        else:
            self.freq = self.freq_list[self.freq_index]

        self.freq_index += 1
        self.message_port_pub(pmt.intern('freq_out'), pmt.cons(pmt.intern('freq'),pmt.to_pmt(self.freq)))
