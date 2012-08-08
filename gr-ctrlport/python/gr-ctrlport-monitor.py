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

from gnuradio import gr, ctrlport

from PyQt4 import QtCore,Qt
import PyQt4.QtGui as QtGui
import sys, time
import Ice
from gnuradio.ctrlport.IceRadioClient import *
from gnuradio.ctrlport.GrDataPlotter import *

_gr_prefs = gr.prefs()
ice_directory = _gr_prefs.get_string('ctrlport', 'ice_directory', '')
print ice_directory
Ice.loadSlice(ice_directory + '/gnuradio.ice')

import GNURadio

class MAINWindow(QtGui.QMainWindow):
    def minimumSizeHint(self):
        return Qtgui.QSize(800,600)

    def __init__(self, radio, port):
        
        super(MAINWindow, self).__init__()
        self.plots = [];

        self.mdiArea = QtGui.QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QtCore.QSignalMapper(self)
        self.windowMapper.mapped[QtGui.QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

#        self.readSettings()

        self.setWindowTitle("GNU Radio Control Port Monitor")
        self.setUnifiedTitleAndToolBarOnMac(True)

#        self.resize(QtCore.QSize(1024,768));      

        self.newCon(radio,port);
#        self.mdiArea.addSubWindow(child);
#        child.resize(QtCore.QSize(800,600));
        icon = QtGui.QIcon( ctrlport.__path__[0] + "/icon.png" );
        self.setWindowIcon(icon);

    def newCon(self,host=None,port=None):
        child = MForm(host,port,self)
        #child.setWindowTitle("Modem Connected :: %s:%s"%(host,port))
        child.setWindowTitle(str(host))
        self.mdiArea.addSubWindow(child)
        child.resize(QtCore.QSize(800,600))
        child.showMaximized()
        return child

    def propertiesMenu(self, key, radio):
        def newUpdaterProxy():
            self.newUpdater(key, radio)

        def newPlotterFProxy():
            self.newPlotF(key)

        def newPlotterCProxy():
            self.newPlotC(key)

        def newPlotterConstProxy():
            self.newPlotConst(key)

        def newPlotterPsdFProxy():
            self.newPlotPsdF(key)

        def newPlotterPsdCProxy():
            self.newPlotPsdC(key)

        menu = QtGui.QMenu(self)
        menu.setTitle("Item Actions")
        menu.setTearOffEnabled(False)

        props = radio.properties([key])

        # object properties
        menu.addAction("Properties", newUpdaterProxy)

        # displays available if not complex
        menu.addAction("Plot Time", newPlotterFProxy)
        menu.addAction("Plot PSD", newPlotterPsdFProxy)

        # displays available if complex
        menu.addAction("Plot Time (cpx)", newPlotterCProxy)
        menu.addAction("Plot Constellation", newPlotterConstProxy)
        menu.addAction("Plot PSD cpx", newPlotterPsdCProxy)

        menu.popup(QtGui.QCursor.pos())

    def newUpdater(self, key, radio):
        updater = UpdaterWindow(key, radio, None)
        updater.setWindowTitle("Updater: " + key)
        updater.setModal(False)
        updater.exec_()

    def newSub(self,e):
        tag = str(e.text(0))
        knobprop = self.knobprops[tag]

        if(knobprop.display == GNURadio.DisplayType.DISPXYSCATTER):
            plot = self.newConstPlot(tag);
            #plot.setSeries(tag,tag);
            #plot.setSeries(tag, knobprop.description);
            #plot.addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);
        elif(knobprop.display == GNURadio.DisplayType.DISPTIMESERIESF):
            plot = self.newPlotF(tag);
            #plot.addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);
        elif(knobprop.display == GNURadio.DisplayType.DISPTIMESERIESC):
            plot = self.newPlotC(tag);
            #plot.addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);
        #plot.setWindowTitle(str(tag));
            
        
    def newPlotConst(self, tag):
        #plot = DataPlotterConst(None,"",'units', '', 250,0,0,120);
        #(self, parent, tag, legend, title, xlabel, ylabel, size, x, y)
        #plot = DataPlotterConst(None, 'legend', 'title', 'xlabel', 'ylabel', 250, 0, 0)
        #self.mdiArea.addSubWindow(plot);
        #plot.dropSignal.connect(self.plotDropEvent );
        #plot.show();

        plot = GrDataPlotterConst(tag, 32e6)
        plot.start();
        self.plots.append(plot);
        return plot;

    def newPlotF(self, tag):
        #plot = DataPlotterTickerWithSeriesButtons(None,"",'units', '', 250,0,0,120)
        #self.mdiArea.addSubWindow(plot.py_window)
        #plot.dropSignal.connect(self.plotDropEvent )
        plot = GrDataPlotterF(tag, 32e6)
        plot.start()
        self.plots.append(plot)
        return plot

    def newPlotC(self, tag):
        plot = GrDataPlotterC(tag, 32e6)
        plot.start()
        self.plots.append(plot)
        return plot     

    def newPlotPsdF(self, tag):
        plot = GrDataPlotterPsdF(tag, 32e6)
        plot.start()
        self.plots.append(plot)
        return plot

    def newPlotPsdC(self, tag):
        plot = GrDataPlotterPsdC(tag, 32e6)
        plot.start()
        self.plots.append(plot)
        return plot     

    def update(self, knobs):
        for plot in self.plots:
            data = knobs[plot.name()].value
            plot.update(data)
            plot.stop()
            plot.wait()
            plot.start()

    def plotDropEvent(self, e):
        model = QtGui.QStandardItemModel()
        model.dropMimeData(e.mimeData(), QtCore.Qt.CopyAction,0,0,QtCore.QModelIndex())
        tag =  str(QtGui.QTreeWidgetItem([model.item(0,0).text()]).text(0));
        knobprop = self.knobprops[tag]
        #self.sender().addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);


    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)


    def createActions(self):
        self.newConAct = QtGui.QAction("&New Connection",
                self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new file", triggered=self.newCon)
        #self.newAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'), "&New Plot",
        self.newPlotAct = QtGui.QAction("&New Plot",
                self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new file", triggered=self.newPlotF)

#        self.openAct = QtGui.QAction(QtGui.QIcon(':/images/open.png'),
#                "&Open...", self, shortcut=QtGui.QKeySequence.Open,
#                statusTip="Open an existing file", triggered=self.open)

#        self.saveAct = QtGui.QAction(QtGui.QIcon(':/images/save.png'),
#                "&Save", self, shortcut=QtGui.QKeySequence.Save,
#                statusTip="Save the document to disk", triggered=self.save)

#        self.saveAsAct = QtGui.QAction("Save &As...", self,
#                shortcut=QtGui.QKeySequence.SaveAs,
#                statusTip="Save the document under a new name",
#                triggered=self.saveAs)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=QtGui.qApp.closeAllWindows)

#        self.cutAct = QtGui.QAction(QtGui.QIcon(':/images/cut.png'), "Cu&t",
#                self, shortcut=QtGui.QKeySequence.Cut,
#                statusTip="Cut the current selection's contents to the clipboard",
#                triggered=self.cut)

#        self.copyAct = QtGui.QAction(QtGui.QIcon(':/images/copy.png'),
#                "&Copy", self, shortcut=QtGui.QKeySequence.Copy,
#                statusTip="Copy the current selection's contents to the clipboard",
#                triggered=self.copy)

#        self.pasteAct = QtGui.QAction(QtGui.QIcon(':/images/paste.png'),
#                "&Paste", self, shortcut=QtGui.QKeySequence.Paste,
#                statusTip="Paste the clipboard's contents into the current selection",
#                triggered=self.paste)

        self.closeAct = QtGui.QAction("Cl&ose", self, shortcut="Ctrl+F4",
                statusTip="Close the active window",
                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QtGui.QAction("Close &All", self,
                statusTip="Close all the windows",
                triggered=self.mdiArea.closeAllSubWindows)


        qks = QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_T);
        self.tileAct = QtGui.QAction("&Tile", self,
                statusTip="Tile the windows",
                triggered=self.mdiArea.tileSubWindows,
                shortcut=qks)

        qks = QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_C);
        self.cascadeAct = QtGui.QAction("&Cascade", self,
                statusTip="Cascade the windows", shortcut=qks,
                triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QtGui.QAction("Ne&xt", self,
                shortcut=QtGui.QKeySequence.NextChild,
                statusTip="Move the focus to the next window",
                triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QtGui.QAction("Pre&vious", self,
                shortcut=QtGui.QKeySequence.PreviousChild,
                statusTip="Move the focus to the previous window",
                triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QtGui.QAction(self)
        self.separatorAct.setSeparator(True)

#        self.aboutAct = QtGui.QAction("&About", self,
#                statusTip="Show the application's About box",
#                triggered=self.about)
#
#        self.aboutQtAct = QtGui.QAction("About &Qt", self,
#                statusTip="Show the Qt library's About box",
#                triggered=QtGui.qApp.aboutQt)
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newConAct)
        self.fileMenu.addAction(self.newPlotAct)
#        self.fileMenu.addAction(self.openAct)
#        self.fileMenu.addAction(self.saveAct)
#        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
#        action = self.fileMenu.addAction("Switch layout direction")
#        action.triggered.connect(self.switchLayoutDirection)
        self.fileMenu.addAction(self.exitAct)

#        self.editMenu = self.menuBar().addMenu("&Edit")
#        self.editMenu.addAction(self.cutAct)
#        self.editMenu.addAction(self.copyAct)
#        self.editMenu.addAction(self.pasteAct)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

#        self.helpMenu = self.menuBar().addMenu("&Help")
#        self.helpMenu.addAction(self.aboutAct)
#        self.helpMenu.addAction(self.aboutQtAct)


    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newConAct)
        self.fileToolBar.addAction(self.newPlotAct)

        self.fileToolBar = self.addToolBar("Window")
        self.fileToolBar.addAction(self.tileAct)
        self.fileToolBar.addAction(self.cascadeAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")


    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
#        self.saveAct.setEnabled(hasMdiChild)
#        self.saveAsAct.setEnabled(hasMdiChild)
#        self.pasteAct.setEnabled(hasMdiChild)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

#        hasSelection = (self.activeMdiChild() is not None and
#                        self.activeMdiChild().textCursor().hasSelection())
#        self.cutAct.setEnabled(hasSelection)
#        self.copyAct.setEnabled(hasSelection)


    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

#        self.fileToolBar.addAction(self.openAct)
#        self.fileToolBar.addAction(self.saveAct)

#        self.editToolBar = self.addToolBar("Edit")
#        self.editToolBar.addAction(self.cutAct)
#        self.editToolBar.addAction(self.copyAct)
#        self.editToolBar.addAction(self.pasteAct)




##class SubscriberPlot(DataPlotterTickerWithSeriesButtons):
#    def __init__(self):
#        super(SubscriberPlot,self).__init__(None, "", 'units', '',250,0,0,120);


class ConInfoDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ConInfoDialog, self).__init__(parent)

        self.gridLayout = QtGui.QGridLayout(self)
        

        self.host = QtGui.QLineEdit(self);
        self.port = QtGui.QLineEdit(self);
        self.host.setText("localhost");
        self.port.setText("43243");

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        self.gridLayout.addWidget(self.host);
        self.gridLayout.addWidget(self.port);
        self.gridLayout.addWidget(self.buttonBox);

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


    def accept(self):
        self.done(1);

    def reject(self):
        self.done(0);


class UpdaterWindow(QtGui.QDialog):
    def __init__(self, key, radio, parent):
        QtGui.QDialog.__init__(self, parent)

        self.key = key;
        self.radio = radio

        self.resize(300,200)
        self.layout = QtGui.QVBoxLayout()

        self.props = radio.properties([key])[key]
        info = str(self.props)

        self.infoLabel = QtGui.QLabel(info)
        self.layout.addWidget(self.infoLabel)

        # Test here to make sure that a 'set' function
        try:
            a = radio.set(radio.get([key]))
            has_set = True
        except Ice.UnknownException:
            has_set = False

        if(has_set is False):
            self.cancelButton = QtGui.QPushButton("Ok")
            self.cancelButton.connect(self.cancelButton, QtCore.SIGNAL('clicked()'), self.reject)

            self.buttonlayout = QtGui.QHBoxLayout()
            self.buttonlayout.addWidget(self.cancelButton)
            self.layout.addLayout(self.buttonlayout)
 
        else: # we have a set function
            self.textInput = QtGui.QLineEdit()
            self.layout.addWidget(self.textInput)

            self.applyButton = QtGui.QPushButton("Apply")
            self.setButton = QtGui.QPushButton("OK")
            self.cancelButton = QtGui.QPushButton("Cancel")

            rv = radio.get([key])
            self.textInput.setText(str(rv[key].value))
            self.sv = rv[key]

            self.applyButton.connect(self.applyButton, QtCore.SIGNAL('clicked()'), self._apply)
            self.setButton.connect(self.setButton, QtCore.SIGNAL('clicked()'), self._set)
            self.cancelButton.connect(self.cancelButton, QtCore.SIGNAL('clicked()'), self.reject)
 
            self.is_num = ((type(self.sv.value)==float) or (type(self.sv.value)==int))
            if(self.is_num):
                self.sliderlayout = QtGui.QHBoxLayout()

                self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)

                self.sliderlayout.addWidget(QtGui.QLabel(str(self.props.min.value)))
                self.sliderlayout.addWidget(self.slider)
                self.sliderlayout.addWidget(QtGui.QLabel(str(self.props.max.value)))

                self.steps = 10000
                self.valspan = self.props.max.value - self.props.min.value
            
                self.slider.setRange(0, 10000)
                self._set_slider_value(self.sv.value)

                self.connect(self.slider, QtCore.SIGNAL("sliderReleased()"), self._slide)

                self.layout.addLayout(self.sliderlayout)

                self.buttonlayout = QtGui.QHBoxLayout()
                self.buttonlayout.addWidget(self.applyButton)
                self.buttonlayout.addWidget(self.setButton)
                self.buttonlayout.addWidget(self.cancelButton)
                self.layout.addLayout(self.buttonlayout)

        # set layout and go...
        self.setLayout(self.layout)
            
    def _set_slider_value(self, val):
        self.slider.setValue(self.steps*(val-self.props.min.value)/self.valspan)
             
    def _slide(self):
        val = (self.slider.value()*self.valspan + self.props.min.value)/float(self.steps)
        self.textInput.setText(str(val))

    def _apply(self):
        if(type(self.sv.value) == str):
            val = str(self.textInput.text())
        elif(type(self.sv.value) == int):
            val = int(round(float(self.textInput.text())))
        elif(type(self.sv.value) == float):
            val = float(self.textInput.text())
        else:
            print "set type not supported! (%s)"%(type(self.sv.value))
            sys.exit(-1)

        self.sv.value = val
        km = {}
        km[self.key] = self.sv
        self.radio.set(km)
        self._set_slider_value(self.sv.value)

    def _set(self):
        self._apply()
        self.done(0)


class MForm(QtGui.QWidget):
    def update(self):
        try:
            st = time.time();
            knobs = self.radio.get([]);
            #print "GOT KNOBS: ", knobs
            ft = time.time();
            latency = ft-st;
            self.parent.statusBar().showMessage("Current GNU Radio Control Port Query Latency: %f ms"%(latency*1000))
            
        except:
            sys.exit(0);
            print "radio.get() failed"
            return;

        tableitems = knobs.keys();
            
        #UPDATE TABLE:
        self.table.updateItems(knobs, self.knobprops)

        #UPDATE PLOTS
        self.parent.update( knobs );


    def __init__(self, radio=None, port=None, parent=None):

        super(MForm, self).__init__()

        if(radio == None or port == None):
            askinfo = ConInfoDialog(self);
            if askinfo.exec_():
                print "connecting..."
                radio = str(askinfo.host.text());
                port = str(askinfo.port.text());
                print "this is broken"
                return;
            else:
                return;
    
        self.parent = parent;
        self.horizontalLayout = QtGui.QVBoxLayout(self);
        self.gridLayout = QtGui.QGridLayout()

        self.radio = radio
        self.knobprops = self.radio.properties([])
        self.parent.knobprops = self.knobprops;
        self.resize(775,500)
        self.timer = QtCore.QTimer()
        self.constupdatediv = 0
        self.tableupdatediv = 0
        plotsize=250

        #print self.knobprops
            
        # make table
        self.table = GrDataPlotterValueTable(self, 0, 0, 400, 200)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.table.treeWidget.setSizePolicy(sizePolicy)
        self.table.treeWidget.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
        self.table.treeWidget.setSortingEnabled(True)
        self.table.treeWidget.setDragEnabled(True)
        
        # add things to layouts
        self.horizontalLayout.addWidget(self.table.treeWidget);

        # set up timer   
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.update)
        self.timer.start(1000)

        # set up context menu .. 
        self.table.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.treeWidget.customContextMenuRequested.connect(self.openMenu)

        # Set up double-click to launch default plotter
        self.connect(self.table.treeWidget,
                     QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'),
                     self.parent.newSub);

    def plotDropEvent(self, e):
        model = QtGui.QStandardItemModel()
        model.dropMimeData(e.mimeData(), QtCore.Qt.CopyAction,0,0,QtCore.QModelIndex())
        tag =  str(QtGui.QTreeWidgetItem([model.item(0,0).text()]).text(0))
        knobprop = self.knobprops[tag]
        #self.sender().addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);

    def openMenu(self, pos):
        index = self.table.treeWidget.selectedIndexes()
        item = self.table.treeWidget.itemFromIndex(index[0])
        itemname = str(item.text(0))
        self.parent.propertiesMenu(itemname, self.radio)
        

class MyClient(IceRadioClient):
    def __init__(self):
        IceRadioClient.__init__(self, MAINWindow)
		
sys.exit(MyClient().main(sys.argv))
