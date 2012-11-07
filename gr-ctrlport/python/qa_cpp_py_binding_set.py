#!/usr/bin/env python
#
# Copyright 2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

# 
# This program tests mixed python and c++ GRCP sets in a single app
#

import Ice
import sys, time, random, numpy
from gnuradio import gr, gr_unittest
import ctrlport_swig as ctrlport

_gr_prefs = gr.prefs()
if(_gr_prefs.has_section('ctrlport')):
    ice_directory = _gr_prefs.get_string('ctrlport', 'ice_directory', '')
    Ice.loadSlice(ice_directory + '/gnuradio.ice')
else:
    for p in sys.path:
        try:
            Ice.loadSlice(p+'/../slice/gnuradio.ice')
        except RuntimeError:
            pass
        else:
            break

import GNURadio

class inc_class:
    def __init__(self,val):
        self.val = val;

    def _get(self):
        #print "returning get (val = %s)"%(str(self.val));
        return self.val;

    def _set(self,val):
        #print "updating val to %s"%(str(val));
        self.val = val;
        return;

getset1 = inc_class(10);
getset2 = inc_class(100.0);
getset3 = inc_class("test");

class test_cpp_py_binding_set(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):

        g1 = ctrlport.RPC_get_int("pyland", "v1", "unit_1_int",
                                  "Python Exported Int", 0, 100, 10,
                                  ctrlport.DISPNULL)
        g1.activate(getset1._get)
        s1 = ctrlport.RPC_get_int("pyland", "v1", "unit_1_int",
                                  "Python Exported Int", 0, 100, 10,
                                  ctrlport.DISPNULL)
        s1.activate(getset1._set)
        time.sleep(0.01)

        # test int variables
        getset1._set(21)
        val = getset1._get()
        rval = g1.get()
        self.assertEqual(val, rval)

        g2 = ctrlport.RPC_get_float("pyland", "v2", "unit_2_float",
                                    "Python Exported Float", -100, 1000.0, 100.0,
                                    ctrlport.DISPNULL)
        g2.activate(getset2._get)
        s2 = ctrlport.RPC_get_float("pyland", "v2", "unit_2_float",
                                    "Python Exported Float", -100, 1000.0, 100.0,
                                    ctrlport.DISPNULL)
        s2.activate(getset2._set)
        time.sleep(0.01)

        # test float variables
        getset2._set(123.456)
        val = getset2._get()
        rval = g2.get()
        self.assertAlmostEqual(val, rval, 4)

        g3 = ctrlport.RPC_get_string("pyland", "v3", "unit_3_string",
                                     "Python Exported String", "", "", "",
                                     ctrlport.DISPNULL)
        g3.activate(getset3._get)
        s3 = ctrlport.RPC_get_string("pyland", "v3", "unit_3_string",
                                     "Python Exported String", "", "", "",
                                     ctrlport.DISPNULL)
        s3.activate(getset3._set)
        time.sleep(0.01)

        # test string variables
        getset3._set("third test")
        val = getset3._get()
        rval = g3.get()
        self.assertEqual(val, rval)


    def test_002(self):
        data = range(1, 10)

        self.src = gr.vector_source_c(data, True)
        self.p = ctrlport.nop(gr.sizeof_gr_complex, 0, 0)
        probe_info = "{0}{1}".format(self.p.name(), self.p.unique_id())

        self.tb.connect(self.src, self.p)

        # Get available endpoint
        ep = ctrlport.rpcmanager_get().endpoints()[0]

        # Initialize a simple Ice client from endpoint
        ic = Ice.initialize(sys.argv)
        base = ic.stringToProxy(ep)
        radio = GNURadio.ControlPortPrx.checkedCast(base)

        self.tb.start()

        # Make sure we have time for flowgraph to run
        time.sleep(0.1)

        # Get all exported knobs
        key_name_a = probe_info+"::a"
        key_name_b = probe_info+"::b"
        ret = radio.get([key_name_a,key_name_b])

        ret[key_name_a].value = 10
        ret[key_name_b].value = 101
        radio.set({key_name_a: ret[key_name_a]})
        radio.set({key_name_b: ret[key_name_b]})

        ret = radio.get([])
        result_a = ret[key_name_a].value
        result_b = ret[key_name_b].value
        self.assertEqual(result_a, 10)
        self.assertEqual(result_b, 101)

        self.tb.stop()
        self.tb.wait()

if __name__ == '__main__':
    gr_unittest.run(test_cpp_py_binding_set, "test_cpp_py_binding_set.xml")

