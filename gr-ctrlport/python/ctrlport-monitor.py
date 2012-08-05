#!/usr/bin/env python

import grcp;

from PyQt4.QtCore import Qt;
#from PyQt4 import QtCore,Qt
from PyQt4 import QtCore
import PyQt4.QtGui as QtGui
import sys, time, Ice, subprocess;
from grcp.IceRadioClient import *;
from grcp.DataPlotter import *;

p1 = subprocess.Popen(["pkg-config", "gnuradio-controlport", "--variable=prefix"],stdout=subprocess.PIPE);
prefix = p1.communicate()[0][:-1];
Ice.loadSlice(prefix + '/include/gnuradio-controlport/gnuradio.ice')

import GNURadio

class MAINWindow(QtGui.QMainWindow):
    def minimumSizeHint(self):
        return Qtgui.QSize(800,600);
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
        icon = QtGui.QIcon( grcp.__path__[0] + "/icon.png" );
        self.setWindowIcon(icon);

# add empty plots ?
#        self.plots = [];
#        for i in range(3):
#            self.newPlot();
    
    def newCon(self,host=None,port=None):
        child = MForm(host,port,self);
        #child.setWindowTitle("Modem Connected :: %s:%s"%(host,port));
        child.setWindowTitle(str(host));
        self.mdiArea.addSubWindow(child);
        child.resize(QtCore.QSize(800,600));
        child.showMaximized();
        return child;


    def newUpd(self,k,r):
        updater = UpdaterWindow(k,r,None);
        updater.setWindowTitle("Updater: " + k);
        self.mdiArea.addSubWindow(updater);
        updater.show();
        

    def newSub(self,e):
        tag = str(e.text(0));
        knobprop = self.knobprops[tag]
        
        if(type(knobprop.min) in [GNURadio.KnobVecB, GNURadio.KnobVecC, GNURadio.KnobVecI,GNURadio.KnobVecF,GNURadio.KnobVecD,GNURadio.KnobVecL]):
            if(knobprop.display == grcp.DISPTIMESERIES):
                #plot = self.newConstPlot();
                plot = self.newVecSeriesPlot();
                plot.setSeries(tag,tag);
                plot.setWindowTitle(str(tag));
            else:   # Plot others as XY for now
                plot = self.newConstPlot();
                plot.setSeries(tag,tag);
                plot.setWindowTitle(str(tag));
        elif(type(knobprop.min) in [GNURadio.KnobB,GNURadio.KnobC,GNURadio.KnobI,GNURadio.KnobF,GNURadio.KnobD,GNURadio.KnobL]):
            plot = self.newPlot();
            plot.addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);
            plot.setWindowTitle(str(tag));
        else:
            print "WARNING: plotting of this knob-type not yet supported, ignoring attempt..."
            
        
    def newVecSeriesPlot(self):
        #plot = DataPlotterEqTaps(None, 'legend', 'title', 'xlabel', 'ylabel', 250, 0, 0, Qt.green)
        plot = DataPlotterVectorOne(None, 'legend', 'title', 'xlabel', 'ylabel', 250, 0, 0);
        self.mdiArea.addSubWindow(plot);
        plot.dropSignal.connect(self.plotDropEvent );
        plot.show();
        self.plots.append(plot);
        return plot;

    def newConstPlot(self):
        plot = DataPlotterConst(None, 'legend', 'title', 'xlabel', 'ylabel', 250, 0, 0)
        self.mdiArea.addSubWindow(plot);
        plot.dropSignal.connect(self.plotDropEvent );
        plot.show();
        self.plots.append(plot);
        return plot;

    def newPlot(self):
        plot = DataPlotterTickerWithSeriesButtons(None,"",'units', '', 250,0,0,120);
        self.mdiArea.addSubWindow(plot);
        plot.dropSignal.connect(self.plotDropEvent );
        plot.show();
        self.plots.append(plot);
        return plot;
        

    def update(self, knobs):
        for item in knobs.keys():
            for plot in self.plots:
#                print "offering key %s val %s to plot %s"%(item, knobs[item].value, plot)
                plot.offerData( knobs[item].value, item );

    def plotDropEvent(self, e):
        model = QtGui.QStandardItemModel()
        model.dropMimeData(e.mimeData(), QtCore.Qt.CopyAction,0,0,QtCore.QModelIndex())
        tag =  str(QtGui.QTreeWidgetItem([model.item(0,0).text()]).text(0));
        knobprop = self.knobprops[tag]
        try:
            self.sender().addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);
        except:
            print "This plot does not accept additional data items! ignoring..."


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
                statusTip="Create a new file", triggered=self.newPlot)

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




class UpdaterWindow(QtGui.QWidget):
    def __init__(self, key, radio, parent):
        QtGui.QWidget.__init__(self,parent)

        self.key = key;
        self.radio = radio;

        self.resize(300,200)
        self.layout = QtGui.QVBoxLayout();

        self.textInput = QtGui.QLineEdit();
        self.setButton = QtGui.QPushButton("Set Value")

        rv = radio.get([key]);
        self.textInput.setText(str(rv[key].value));
        self.sv = rv[key];


        self.props = radio.properties([key])[key];
        info = str(self.props);

        self.infoLabel = QtGui.QLabel(info);
        self.layout.addWidget(self.infoLabel);

        self.layout.addWidget(self.textInput);
 
        self.setButton.connect(self.setButton, QtCore.SIGNAL('clicked()'), self._set)
 
        self.is_num = ((type(self.sv.value)==float) or (type(self.sv.value)==int));
        if(self.is_num):
            self.sliderlayout = QtGui.QHBoxLayout();

            self.slider = QtGui.QSlider(Qt.Horizontal);

            self.sliderlayout.addWidget(QtGui.QLabel(str(self.props.min.value)));
            self.sliderlayout.addWidget(self.slider);
            self.sliderlayout.addWidget(QtGui.QLabel(str(self.props.max.value)));
            

            self.steps = 10000;
            self.valspan = self.props.max.value - self.props.min.value;
            
            #self.slider.setRange( self.props.min.value, self.props.max.value );
            self.slider.setRange( 0,10000 );
            
            self.slider.setValue( self.sv.value );
            self.slider.setValue( self.steps*(self.sv.value-self.props.min.value)/self.valspan);

            #self.slider.setTracking(True);
            #self.connect(self.slider, QtCore.SIGNAL("valueChange(int)"), self._slide);
            self.connect(self.slider, QtCore.SIGNAL("sliderReleased()"), self._slide);

            self.layout.addLayout(self.sliderlayout);

        self.layout.addWidget(self.setButton);

        # set layout and go...
        self.setLayout(self.layout);
                 
    def _slide(self):
        val = (self.slider.value()*self.valspan + self.props.min.value)/float(self.steps);
        self.textInput.setText(str(val));

    def _set(self):
        if(type(self.sv.value) == str):
            val = str(self.textInput.text());
        elif(type(self.sv.value) == int):
            val = int(round(float(self.textInput.text())));
        elif(type(self.sv.value) == float):
            val = float(self.textInput.text());
        else:
            print "set type not supported! (%s)"%(type(self.sv.value));
            sys.exit(-1);
        #self.sv.value = int(val);
        self.sv.value = val;
        km = {};
        km[self.key] = self.sv;
        self.radio.set(km);

class MForm(QtGui.QWidget):
    def update(self):
        try:
            st = time.time();
            knobs = self.radio.get([]);
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
        plotsize=250; 
    
            
        # make table
        self.table = DataPlotterValueTable(self, 0, 0, 400, 200);
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.table.treeWidget.setSizePolicy(sizePolicy);
        self.table.treeWidget.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed);
        self.table.treeWidget.setSortingEnabled(True);
        self.table.treeWidget.setDragEnabled(True)
        
        # add things to layouts
        self.horizontalLayout.addWidget(self.table.treeWidget);
                
        # set up timer   
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.update);
        self.connect(self.table.treeWidget, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.parent.newSub);

        # set up context menu .. 
        self.table.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu);
        self.table.treeWidget.customContextMenuRequested.connect(self.openMenu);

        self.timer.start(2000)

    def plotDropEvent(self, e):
        model = QtGui.QStandardItemModel()
        model.dropMimeData(e.mimeData(), QtCore.Qt.CopyAction,0,0,QtCore.QModelIndex())
        tag =  str(QtGui.QTreeWidgetItem([model.item(0,0).text()]).text(0));
        knobprop = self.knobprops[tag]
        self.sender().addSeriesWithButton(tag, knobprop.description + ' (' + knobprop.units + ')', None, 1.0);

    def openMenu(self, pos):
        index = self.table.treeWidget.selectedIndexes();
        item = self.table.treeWidget.itemFromIndex(index[0]);
        itemname = str(item.text(0));
        self.parent.newUpd(itemname, self.radio);
#        updater = UpdaterWindow(itemname, self.radio, self.parent);
#        updater.setWindowTitle("Updater: " + itemname);
#        self.parent.mdiArea.addSubWindow(updater);
#        print "done"


class MyClient(IceRadioClient):
    def __init__(self): IceRadioClient.__init__(self, MAINWindow)
		
sys.exit(MyClient().main(sys.argv))
