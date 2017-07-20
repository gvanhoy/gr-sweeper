#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Uhdgps Rssi Log
# Generated: Wed Jul 19 14:53:36 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import es
import pmt
import sweeper
import time
import uhdgps


class uhdgps_rssi_log(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Uhdgps Rssi Log")

        ##################################################
        # Variables
        ##################################################
        self.step = step = 6e6
        self.samp_rate = samp_rate = 200e3
        self.gain = gain = 30
        self.end_frequency = end_frequency = 842e6
        self.center_frequency = center_frequency = 493e6
        self.begin_frequency = begin_frequency = 493e6

        ##################################################
        # Blocks
        ##################################################
        self.uhdgps_meta_to_json_file_0_0 = uhdgps.meta_to_json_file('/tmp/WAMU_RSSI.locked_%(hostname)s_%(time)s.json')
        self.uhdgps_meta_to_json_file_0 = uhdgps.meta_to_json_file('/tmp/WAMU_RSSI_%(hostname)s_%(time)s.json')
        self.uhdgps_gps_probe_e310_0 = uhdgps.gps_probe_e310(self, 'uhd_usrp_source_0')
        self.uhdgps_cpdu_average_power_0 = uhdgps.cpdu_average_power(-60)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "type=e3x0")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(center_frequency, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.sweeper_sweeper_0 = sweeper.sweeper(begin_frequency, step, end_frequency)
        self.es_trigger_sample_timer_0 = es.trigger_sample_timer(gr.sizeof_gr_complex, int(samp_rate), 1024, int(samp_rate), 512 )
        self.es_sink_0 = es.sink(1*[gr.sizeof_gr_complex],8,64,2,2,0)
        self.es_handler_pdu_0 = es.es_make_handler_pdu(es.es_handler_print.TYPE_C32)
        self.blocks_pdu_remove_0 = blocks.pdu_remove(pmt.intern("es::event_buffer"))
        self.blocks_pdu_filter_0 = blocks.pdu_filter(pmt.to_pmt("gps_locked"), pmt.to_pmt("true"), False)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.sweeper_sweeper_0, 'clock'))
        self.msg_connect((self.blocks_pdu_filter_0, 'pdus'), (self.uhdgps_meta_to_json_file_0_0, 'pdus'))
        self.msg_connect((self.blocks_pdu_remove_0, 'pdus'), (self.uhdgps_gps_probe_e310_0, 'pdus'))
        self.msg_connect((self.es_handler_pdu_0, 'pdus_out'), (self.uhdgps_cpdu_average_power_0, 'cpdus'))
        self.msg_connect((self.es_trigger_sample_timer_0, 'sample_timer_event'), (self.es_handler_pdu_0, 'handle_event'))
        self.msg_connect((self.es_trigger_sample_timer_0, 'which_stream'), (self.es_sink_0, 'schedule_event'))
        self.msg_connect((self.sweeper_sweeper_0, 'msg_out'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.uhdgps_cpdu_average_power_0, 'cpdus'), (self.blocks_pdu_remove_0, 'pdus'))
        self.msg_connect((self.uhdgps_gps_probe_e310_0, 'pdus'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.uhdgps_gps_probe_e310_0, 'pdus'), (self.blocks_pdu_filter_0, 'pdus'))
        self.msg_connect((self.uhdgps_gps_probe_e310_0, 'pdus'), (self.uhdgps_meta_to_json_file_0, 'pdus'))
        self.connect((self.es_trigger_sample_timer_0, 0), (self.es_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.es_trigger_sample_timer_0, 0))

    def get_step(self):
        return self.step

    def set_step(self, step):
        self.step = step

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)


    def get_end_frequency(self):
        return self.end_frequency

    def set_end_frequency(self, end_frequency):
        self.end_frequency = end_frequency

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.uhd_usrp_source_0.set_center_freq(self.center_frequency, 0)

    def get_begin_frequency(self):
        return self.begin_frequency

    def set_begin_frequency(self, begin_frequency):
        self.begin_frequency = begin_frequency


def main(top_block_cls=uhdgps_rssi_log, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
