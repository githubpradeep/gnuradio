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
# This program tests mixed python and c++ ControlPort exports in a single app
#

import ctrlport_swig as ctrlport;
import sys;
import Ice;
import time;
from gnuradio import gr;
from ctrlport.monitor import *;

src = gr.file_source(gr.sizeof_gr_complex, "/dev/urandom");
th = gr.throttle(gr.sizeof_gr_complex, 1024);
p1 = ctrlport.probe_c("aaa","C++ exported variable");
p2 = ctrlport.probe_c("bbb","C++ exported variable");
tb = gr.top_block();
tb.connect(src, th, p1);
tb.connect(th, p2);
tb.start();



def get1():
    return "success"

def get2():
    return "failure"

class inc_class:
    def __init__(self):
        self.val = 1;
    def pp(self):
        self.val = self.val+1;
        return self.val;
get3 = inc_class();

def get4():
    rv = time.time();
    return rv;

v1 = ctrlport.RPC_get_string("pyland","v1","unit_1_string","Python Exported String","","","",ctrlport.DISPNULL);
v1.activate(get1);

v2 = ctrlport.RPC_get_string("pyland","v2","unit_2_string","Python Exported String","","","",ctrlport.DISPNULL);
v2.activate(get2);

v3 = ctrlport.RPC_get_int("pyland","v3","unit_3_int","Python Exported Int",0,100,1,ctrlport.DISPNULL);
v3.activate(get3.pp);

v4 = ctrlport.RPC_get_double("pyland","time","unit_4_time_double","Python Exported Double",0,1000,1,ctrlpor.DISPNULL);
v4.activate(get4);

#print ctrlport.Instance.get_communicator();

# print some variables locally
rval =  v1.get()  
print rval;
rval =  v2.get()  
print rval;

# Launch ControlPort Monitor Application
monitor_app = monitor();

# Wait for GUI to close
monitor_app.proc.wait();

# Stop GR graph
tb.stop();

