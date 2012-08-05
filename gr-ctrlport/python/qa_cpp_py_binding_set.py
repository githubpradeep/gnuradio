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
tb = gr.top_block();
tb.connect(src, th, p1);
tb.start();


class inc_class:
    def __init__(self,val):
        self.val = val;

    def _get(self):
        print "returning get (val = %s)"%(str(self.val));
        return self.val;

    def _set(self,val):
        print "updating val to %s"%(str(val));
        self.val = val;
        return;

getset1 = inc_class(10);
getset2 = inc_class(100.0);
getset3 = inc_class("test");

#print getset1._get();

g1 = grcp.RPC_get_int("pyland","v1","unit_1_int","Python Exported Int",0,100,10,grcp.DISPNULL);
g1.activate(getset1._get);
s1 = grcp.RPC_set_int("pyland","v1","unit_1_int","Python Exported Int",0,100,10,grcp.DISPNULL);
s1.activate(getset1._set);

g2 = grcp.RPC_get_float("pyland","v2","unit_2_float","Python Exported Int",-100,1000.0,100.0,grcp.DISPNULL);
g2.activate(getset2._get);
s2 = grcp.RPC_set_float("pyland","v2","unit_2_float","Python Exported Int",-100,1000.0,100.0,grcp.DISPNULL);
s2.activate(getset2._set);

g3 = grcp.RPC_get_string("pyland","v3","unit_3_string","Python Exported Int","","","",grcp.DISPNULL);
g3.activate(getset3._get);
s3 = grcp.RPC_set_string("pyland","v3","unit_3_string","Python Exported Int","","","",grcp.DISPNULL);
s3.activate(getset3._set);

# Launch GRCP Monitor Application
monitor_app = GRCPMonitor();

# Wait for GUI to close
monitor_app.proc.wait();

# Stop GR graph
tb.stop();

