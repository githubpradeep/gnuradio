
from PyQt4 import Qt, QtGui, QtCore
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *

class Zoomer(Qwt.QwtPlotZoomer):
    def __init__(self, a,b,c,d,e):
        Qwt.QwtPlotZoomer.__init__(self,a,b,c,d,e);
        self.zoomers = [];

    def zoom(self, r):
        Qwt.QwtPlotZoomer.zoom(self,r);
        if(r == 0):
            #self.plot().setAxisAutoScale(True);
            self.plot().setAxisAutoScale(Qwt.QwtPlot.xBottom)
            self.plot().setAxisAutoScale(Qwt.QwtPlot.yLeft)
            self.plot().replot();


class DataPlotterBase(Qwt.QwtPlot):
    DefaultColors = ( Qt.Qt.green, Qt.Qt.red, Qt.Qt.blue,
              Qt.Qt.cyan, Qt.Qt.magenta, Qt.Qt.black, Qt.Qt.darkRed, 
	      Qt.Qt.darkGray, Qt.Qt.darkGreen, Qt.Qt.darkBlue, Qt.Qt.yellow)

    dropSignal = QtCore.pyqtSignal(QtCore.QEvent)
 
    def contextMenuEvent(self,e):
        menu = QtGui.QMenu(self);
        menu.addAction(self.gridAct);
        menu.addAction(self.axesAct);
#        print dir(menu);
        menu.exec_(e.globalPos());
#        print "context menu event!"
#        print e;

    def dragEnterEvent(self,e):
        e.accept();

    def dropEvent(self, e):
        Qwt.QwtPlot.dropEvent(self,e)
        self.dropSignal.emit( e );



    def __init__(self, parent, title, xlabel, ylabel, size, x, y):
        Qwt.QwtPlot.__init__(self, parent)
        self.callback = None;

#        self.newPlotAct = QtGui.QAction("&New Plot",
#                self, shortcut=QtGui.QKeySequence.New,
#                statusTip="Create a new file", triggered=self.newPlot)
        self.gridAct = QtGui.QAction("Toggle &Grid", self, triggered=self.toggleGrid);
        self.axesAct = QtGui.QAction("Toggle &Axes", self, triggered=self.toggleAxes);

        # Set up the zoomer   
        self.zoomer = Zoomer(Qwt.QwtPlot.xBottom,
                                        Qwt.QwtPlot.yLeft,
                                        Qwt.QwtPicker.DragSelection,
                                        Qwt.QwtPicker.AlwaysOff,
                                        self.canvas())

        # Crosshairs + Data labels
        self.picker = Qwt.QwtPlotPicker(
            Qwt.QwtPlot.xBottom,
            Qwt.QwtPlot.yLeft,
            Qwt.QwtPicker.PointSelection | Qwt.QwtPicker.DragSelection,
            Qwt.QwtPlotPicker.CrossRubberBand,
            Qwt.QwtPicker.AlwaysOn,
            self.canvas())
        self.picker.setRubberBandPen(QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.DashLine))
        self.picker.setTrackerPen(QtGui.QPen(QtCore.Qt.white))

        self.axisEnable = False;
        # Turn off bloated data labels
        self.enableAxis(Qwt.QwtPlot.yLeft, False);
        self.enableAxis(Qwt.QwtPlot.xBottom, False);

        # Allow panning with middle mouse
        panner = Qwt.QwtPlotPanner(self.canvas())
        panner.setAxisEnabled(Qwt.QwtPlot.yRight, False)
        panner.setMouseButton(Qt.Qt.MidButton)

        # Accept dropping of stats
        self.setAcceptDrops(True);
        self.grid = None
        self.setCanvasBackground(Qt.Qt.black)

#        self.alignScales()
        #        self.x = arange(-1.5, 100.1, 1.5)
        #        self.y = zeros(len(self.x), Float)
        #self.setTitle(title)
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.TopLegend);
                #self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);
        #        self.curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.XCross,
        #                Qt.QBrush(), Qt.QPen(Qt.Qt.blue), Qt.QSize(3, 3)))
        
        #        self.curve.setStyle(Qwt.QwtPlotCurve.NoCurve)

#        mY = Qwt.QwtPlotMarker()
#        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
#        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
#        mY.setYValue(0.0)
#        mY.attach(self)

#AAA
#        self.axisEnabled(False);
        self.axisEnabled(True);

        #self.setAxisTitle(Qwt.QwtPlot.xBottom, xlabel)
        #self.setAxisTitle(Qwt.QwtPlot.yLeft, ylabel)
        self.resize(size, size)
#        self.setGeometry(x, y, size, size)
        self.setAutoReplot(False)
        self.show()
        self.updateTimerInt = 500
        self.startTimer(self.updateTimerInt)
    
        #self.toggleGrid();
        self.toggleAxes();

#    def alignScales(self):
#        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
#        self.canvas().setLineWidth(1)
#        for i in range(Qwt.QwtPlot.axisCnt):
#            scaleWidget = self.axisWidget(i)
#            if scaleWidget:
#                scaleWidget.setMargin(0)
#            scaleDraw = self.axisScaleDraw(i)
##            scaleDraw = False;
#            if scaleDraw:
#                scaleDraw.enableComponent(
#                    Qwt.QwtAbstractScaleDraw.Backbone, False)

    def toggleAxes(self):
        self.axisEnable = not self.axisEnable;
        self.enableAxis(Qwt.QwtPlot.yLeft, self.axisEnable);
        self.enableAxis(Qwt.QwtPlot.xBottom, self.axisEnable);


    def toggleGrid(self):
        # grid
        if self.grid == None:
            self.grid = Qwt.QwtPlotGrid()
            self.grid.enableXMin(True)
            self.grid.setMajPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.DotLine))
            self.grid.setMinPen(Qt.QPen(Qt.Qt.gray, 0 , Qt.Qt.DotLine))
            self.grid.attach(self)
        else:
            self.grid.detach()
            self.grid = None

    	return self

class DataPlotterVector(DataPlotterBase):
    def __init__(self, parent, legend, title, xlabel, ylabel, size, x, y):
        DataPlotterBase.__init__(self, parent, title, xlabel, ylabel, size, x, y)
        self.curve = Qwt.QwtPlotCurve(legend)
        self.curve.attach(self)
        self.tag = None;

    #def offerDataComplexVector(self, data):
    #      self.x = data[::2]; self.y = data[1::2]
    def offerData(self, data, tag):
        if(tag == self.tag):
            self.x = data[::2]; self.y = data[1::2]

    def timerEvent(self, e):
        self.curve.setData(self.x, self.y)
        self.replot()

    def enableLegend(self):
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);
        return self

    def setSeries(self,tag,name):
        self.tag = tag;
        self.curve.setTitle(name)


class DataPlotterConst(DataPlotterVector):
    def __init__(self, parent, legend, title, xlabel, ylabel, size, x, y):
        DataPlotterVector.__init__(self, parent, legend, title, xlabel, ylabel, size, x, y)
        self.x = arange(-2, 100.1, 2)
        self.y = zeros(len(self.x), Float)
#       #self.curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.NoSymbol,
#        	Qt.QBrush(), Qt.QPen(Qt.Qt.blue), Qt.QSize(1, 1)))
        self.curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.XCross,
        	Qt.QBrush(), Qt.QPen(Qt.Qt.green), Qt.QSize(2, 2)))
        self.curve.setStyle(Qwt.QwtPlotCurve.NoCurve)
        self.setAxisAutoScale(False)
        #self.setAxisAutoScale(False)

class DataPlotterEqTaps(DataPlotterVector):
    def __init__(self, parent, legend, title, xlabel, ylabel, size, x, y, qtcolor):
	DataPlotterVector.__init__(self, parent, legend, title, xlabel, ylabel, size, x, y)
        self.x = arange(-.5, .5, 1)
        self.y = zeros(len(self.x), Float)
        self.curve.setPen(Qt.QPen(qtcolor))

class DataPlotterTicker(DataPlotterBase):
    def __init__(self, parent, title, xlabel, ylabel, size, x, y, seconds = 60):
    	DataPlotterBase.__init__(self, parent, title, xlabel, ylabel, size, x, y)
    	self.series = {}
    	self.setTimeScale(seconds)

# AAAAAAAAAA - enable for legend at bottom
#        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);
    	self.skipEvents=1

    def setTimeScale(self, seconds):
	intv =  float(self.updateTimerInt) / 1000
        self.x = arange(0, seconds, intv)
        #self.x = arange(0, seconds, 1)
	return self

    def addSeries(self, tag, label, qtcolor = None, alpha = 1):
    	class Series:
    		def __init__(self, tag, label, qtcolor, x, plot):
    			self.vec =  zeros(len(x), Float)
    			self.value = None
    			self.alpha = alpha
    			self.curve = Qwt.QwtPlotCurve(label)
    			self.curve.setPen(Qt.QPen(qtcolor))
    			self.plot = plot
    
    	if qtcolor == None: qtcolor = self.DefaultColors[len(self.series)]
    	self.series[tag] = s = Series(tag, label, qtcolor, self.x, self)
    	self.enableSeries(tag)
    	return self

    def enableSeries(self, tag):
    	if self.hasSeries(tag):
    		s = self.series[tag]
    		s.enabled = True
            	s.curve.attach(s.plot)
    	return self

    def disableSeries(self, tag):
    	if self.hasSeries(tag):
    		s = self.series[tag]
    		s.enabled = False 
            	s.curve.detach()
    	return self

    def toggleSeries(self,tag):
    	if self.seriesIsEnabled(tag):
    		self.disableSeries(tag)
    	else:
    		self.enableSeries(tag)
    	return self

    def timerEvent(self, e):
        for k, v in self.series.iteritems():
            if v.value == None: continue
            elif v.vec[0] == 0: v.vec =  ones(len(v.vec), Float)*v.value
	
            prev = v.vec[0]
            v.vec = concatenate((v.vec[:1], v.vec[:-1]), 1)
            v.vec[0] = v.value*v.alpha + prev*(1-v.alpha)
            self.series[k] = v 
            v.curve.setData(self.x, v.vec)
            self.replot()

    def offerData(self, value, tag):
        if(self.series.has_key(tag)):
            if not value == NaN:
            	self.series[tag].value = value
                #print "Data Offer %s items:"%(tag)
        return self

    def hasSeries(self, tag):
	       return self.series.has_key(tag);

    def seriesIsEnabled(self, tag):
    	if self.hasSeries(tag): return self.series[tag].enabled 
    	else: return False

class DataPlotterTickerWithSeriesButtons(DataPlotterTicker):
    def __init__(self, parent, title, xlabel, ylabel, size, x, y, seconds = 60):
        DataPlotterTicker.__init__(self, parent, title, xlabel, ylabel, size, x, y, seconds)
        DataPlotterTicker.setAcceptDrops(self,True);
    	self.buttonx = 50; self.buttony = 20; self.buttonSize = 16 
    	self.btns = [] 




    def addSeriesWithButton(self, tag, legend, qtcolor=None, alpha = 1):
    	self.addSeries(tag, legend, qtcolor, alpha)
    	lenbtns = len(self.btns)
    
        btn = Qt.QToolButton(self)
    	btn.rank = lenbtns
        btn.setText(str(btn.rank))
    	btn.tag = tag
        #btn.setIcon(Qt.QIcon(Qt.QPixmap(print_xpm)))
        #btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    	#btn.setForegroundColor(Qt.Qt.red)
    	self.btns.append(btn)
    	btn.setGeometry(self.buttonx, self.buttony, self.buttonSize, self.buttonSize)
    	self.buttonx += self.buttonSize
    
    	if lenbtns == 0: callback = self.print_0
    	if lenbtns == 1: callback = self.print_1
    	if lenbtns == 2: callback = self.print_2
    	if lenbtns == 3: callback = self.print_3
    	if lenbtns == 4: callback = self.print_4
    	if lenbtns == 5: callback = self.print_5
    	if lenbtns == 6: callback = self.print_6
    	if lenbtns == 7: callback = self.print_7
        self.connect(btn, Qt.SIGNAL('clicked()'), callback)
    	return self

    def toggleSeriesWithButton(self,btn):
    	DataPlotterTicker.toggleSeries(self, btn.tag)
    
    	if self.seriesIsEnabled(btn.tag):
    #		btn.setForegroundRole(Qt.QPalette.NoRole)
    		btn.setText(str(btn.rank))
    	else:
    		btn.setText('x')
    #		btn.setForegroundRole(Qt.QPalette.Light)
    
    def print_0(self): self.toggleSeriesWithButton(self.btns[0])
    def print_1(self): self.toggleSeriesWithButton(self.btns[1])
    def print_2(self): self.toggleSeriesWithButton(self.btns[2])
    def print_3(self): self.toggleSeriesWithButton(self.btns[3])
    def print_4(self): self.toggleSeriesWithButton(self.btns[4])
    def print_5(self): self.toggleSeriesWithButton(self.btns[5])
    def print_6(self): self.toggleSeriesWithButton(self.btns[6])
    def print_7(self): self.toggleSeriesWithButton(self.btns[7])

class DataPlotterValueTable:
    def __init__(self, parent, x, y, xsize, ysize, headers=['Statistic Key ( Source Block :: Stat Name )  ', 'Curent Value', 'Units', 'Description']):
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
            items.append(QtGui.QTreeWidgetItem([str(k), str(v.value), knobprops[k].units, knobprops[k].description]))
        self.treeWidget.insertTopLevelItems(0, items)
