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

import Ice, Glacier2
from PyQt4 import QtGui, QtCore
import sys, time, Ice
from gnuradio import gr

_gr_prefs = gr.prefs()
ice_directory = _gr_prefs.get_string('ctrlport', 'ice_directory', '')
Ice.loadSlice(ice_directory + '/gnuradio.ice')

import GNURadio

class IceRadioClient(Ice.Application):
    def __init__(self, parentClass):
        self.parentClass = parentClass

    def run(self,args):
        if len(args) < 2:
                print "useage: [glacierinstance glacierhost glacierport] host port"
                return
        if len(args) == 8:
                self.useglacier = True
		guser = args[1]
                gpass = args[2]
                ginst = args[3]
                ghost = args[4]
                gport = args[5]
                host = args[6]
                port = args[7]
        else:
                self.useglacier = False
                host = args[1]
                port = args[2]

        if self.useglacier:
	  gstring = ginst + "/router -t:tcp -h " + ghost + " -p " + gport
	  print "GLACIER: {0}".format(gstring)
	  
	  setrouter = Glacier2.RouterPrx.checkedCast(self.communicator().stringToProxy(gstring))
	  self.communicator().setDefaultRouter(setrouter)
          defaultRouter = self.communicator().getDefaultRouter()
	  #defaultRouter = self.communicator().stringToProxy(gstring)
          if not defaultRouter:
              print self.appName() + ": no default router set"
              return 1
	  else:
              print str(defaultRouter)
          router = Glacier2.RouterPrx.checkedCast(defaultRouter)
          if not router:
              print self.appName() + ": configured router is not a Glacier2 router"
              return 1

          while True:
            print "This demo accepts any user-id / password combination."
	    if not guser == '' and not gpass == '':
		id = guser
                pw = gpass
	    else:
            	id = raw_input("user id: ")
                pw = raw_input("password: ")

            try:
                router.createSession(id, pw)
                break
            except Glacier2.PermissionDeniedException, ex:
                print "permission denied:\n" + ex.reason

        base = self.communicator().stringToProxy("gnuradio -t:tcp -h " + host + " -p " + port).ice_twoway().ice_timeout(-1)
        radio = GNURadio.ControlPortPrx.checkedCast(base)

        if not radio:
            print args[0] + ": invalid proxy"; return 1

        app = QtGui.QApplication(sys.argv)
        ex = self.parentClass(radio, port)
        ex.show();
        app.exec_()
