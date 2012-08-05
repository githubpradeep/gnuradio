#!/usr/bin/env python

# 
# This program tests mixxed python and c++ GRCP exports in a single app
#

import grcp;
import sys;
import Ice;
import time;
from gnuradio import gr;
from grcp.GRCPMonitor import *;

src = gr.file_source(gr.sizeof_gr_complex, "/dev/urandom");
th = gr.throttle(gr.sizeof_gr_complex, 1024);
p1 = grcp.probe_c("aaa","C++ exported variable");
p2 = grcp.probe_c("bbb","C++ exported variable");
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

v1 = grcp.RPC_get_string("pyland","v1","unit_1_string","Python Exported String","","","",grcp.DISPNULL);
v1.activate(get1);

v2 = grcp.RPC_get_string("pyland","v2","unit_2_string","Python Exported String","","","",grcp.DISPNULL);
v2.activate(get2);

v3 = grcp.RPC_get_int("pyland","v3","unit_3_int","Python Exported Int",0,100,1,grcp.DISPNULL);
v3.activate(get3.pp);

v4 = grcp.RPC_get_double("pyland","time","unit_4_time_double","Python Exported Double",0,1000,1,grcp.DISPNULL);
v4.activate(get4);

#print grcp.Instance.get_communicator();

# print some variables locally
rval =  v1.get()  
print rval;
rval =  v2.get()  
print rval;

# Launch GRCP Monitor Application
monitor_app = GRCPMonitor();

# Wait for GUI to close
monitor_app.proc.wait();

# Stop GR graph
tb.stop();

