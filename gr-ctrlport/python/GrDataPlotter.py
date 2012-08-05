#!/usr/bin/env python
#
# Copyright 2011 Free Software Foundation, Inc.
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

from gnuradio import gr
import sys, time

try:
    from gnuradio import qtgui
    from PyQt4 import QtGui, QtCore
    import sip
except ImportError:
    print "Error: Program requires PyQt4 and gr-qtgui."
    sys.exit(1)

class GrDataPlotter(gr.top_block):
    def __init__(self, name, rate):
        gr.top_block.__init__(self)

        self.h = open('/tmp/grplotter.log', 'w')
        self.h.write("{0}: CREATED NEW GRDATAPLOTTER\n".format(time.asctime()))

        self._name = name
        self._npts = 500
        samp_rate = 1.0

        self._last_data = self._npts*[0,]
        self._data_len = 0

        self.src = gr.vector_source_c([])
        self.thr = gr.throttle(gr.sizeof_gr_complex, rate)
        self.snk = qtgui.time_sink_c(self._npts, samp_rate,
                                     self._name, 1)

        self.connect(self.src, self.thr, (self.snk, 0))

        self.py_window = sip.wrapinstance(self.snk.pyqwidget(), QtGui.QWidget)
        self.py_window.show()

    def __del__(self):
            self.h.write("{0}: CLOSING FILE\n".format(time.asctime()))
            self.h.close()

    def name(self):
        return self._name

    def update(self, data):
        # Ask GUI if there has been a change in nsamps
        npts = self.snk.nsamps()
        if(self._npts != npts):

            # Adjust buffers to accomodate new settings
            if(npts < self._npts):
                if(self._data_len < npts):
                    self._last_data = self._last_data[0:npts]
                else:
                    self._last_data = self._last_data[self._data_len-npts:self._data_len]
                    self._data_len = npts
            else:
                self._last_data += (npts - self._npts)*[0,]
            self._npts = npts
            self.snk.reset()
        
        # Update the plot data depending on type
        if(type(data) == list):
            if(len(data) > self._npts):
                self.src.set_data(data)
                self._last_data = data[-self._npts:]
            else:
                newdata = self._last_data[-(self._npts-len(data)):]
                newdata += data
                self.src.set_data(new_data)
                self._last_data = newdata

        else: # single value update
            if(self._data_len < self._npts):
                self._last_data[self._data_len] = data
                self._data_len += 1
            else:
                self._last_data = self._last_data[1:]
                self._last_data.append(data)
            self.src.set_data(self._last_data)

class GrDataPlotterValueTable:
    def __init__(self, parent, x, y, xsize, ysize,
                 headers=['Statistic Key ( Source Block :: Stat Name )  ',
                          'Curent Value', 'Units', 'Description']):
	# must encapsulate, cuz Qt's bases are not classes
        self.treeWidget = QtGui.QTreeWidget(parent)
        self.treeWidget.setColumnCount(len(headers))
        self.treeWidget.setGeometry(x,y,xsize,ysize)
        self.treeWidget.setHeaderLabels(headers)
        self.treeWidget.resizeColumnToContents(0)

    def updateItems(self, knobs, knobprops):
        items = [];
        self.treeWidget.clear()
        for k, v in knobs.iteritems():
            items.append(QtGui.QTreeWidgetItem([str(k), str(v.value),
                                                knobprops[k].units,
                                                knobprops[k].description]))
        self.treeWidget.insertTopLevelItems(0, items)