/*
 * Copyright 2012 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

[["python:package:gnuradio.ctrlport"]]

#ifndef GNURADIO_DEBUG
#define GNURADIO_DEBUG

module GNURadio {
class Knob {};
class KnobB extends Knob { bool   value; };
class KnobC extends Knob { byte   value; };
class KnobI extends Knob { int 	  value; };
class KnobF extends Knob { float  value; };
class KnobD extends Knob { double value; };
class KnobL extends Knob { long   value; };
class KnobS extends Knob { string value; };

sequence<bool>   VectorB; sequence<byte>   VectorC; 
sequence<int>    VectorI; sequence<float>  VectorF;
sequence<double> VectorD; sequence<string> VectorS;
sequence<long> 	 VectorL;

class KnobVecB extends Knob { VectorB value; }; 
class KnobVecC extends Knob { VectorC value; }; 
class KnobVecI extends Knob { VectorI value; }; 
class KnobVecF extends Knob { VectorF value; }; 
class KnobVecD extends Knob { VectorD value; }; 
class KnobVecL extends Knob { VectorL value; }; 
class KnobVecS extends Knob { VectorS value; }; 

enum KnobType { KNOBBOOL, 	KNOBCHAR, 	KNOBINT, 	KNOBFLOAT, 
		KNOBDOUBLE, 	KNOBSTRING, 	KNOBLONG, 	KNOBVECBOOL, 
		KNOBVECCHAR, 	KNOBVECINT,	KNOBVECFLOAT, 	KNOBVECDOUBLE, 
		KNOBVECSTRING, 	KNOBVECLONG };

enum DisplayType {
  DISPNULL, 
  DISPTIMESERIESF,
  DISPTIMESERIESC,
  DISPXYSCATTER,
  DISPXYLINE
};

struct KnobProp {
	KnobType    type;
	string      units;
	string      description;
        DisplayType display;
	Knob        min;
	Knob        max;
	Knob        defaultvalue;
};

sequence<string> 		KnobIDList;
dictionary<string, Knob> 	KnobMap;
dictionary<string, KnobProp> 	KnobPropMap;
dictionary<string, string>	WaveformArgMap;

interface StreamReceiver {
    void 			push(VectorC 	data);
};

interface ControlPort {
    void 			set(KnobMap knobs);
    idempotent  KnobMap 	get(KnobIDList knobs);
    idempotent  KnobPropMap 	properties(KnobIDList knobs);
    void 			shutdown();

//    string 			subscribe(StreamReceiver* proxy, string streamName, int requestedPeriod, int RequestedSize);
//    idempotent  void 		unsubscribe(string streamID);
};

struct FeedInfo {
	string protocol;
	string address;
	string iface;
	string port;
};

//TODO: convert this part to a Feed Info
struct ReceiverInfo {
	string uid;
	string signalType;
	string signalName;
	string allocatableObjectID;
	string signalProtocol;
	string signalAddress;
	string signalInterface;
	string signalPort;
};

interface Component {
		void setName(string newName);
};

module Frontend {
	interface AbstractReceiver extends Component {
        idempotent ReceiverInfo   getReceiverInfo();
	};
};

module Booter {
    dictionary<string, string>      WaveformArgs;

    exception WaveformRunningError {
        string waveformClass;
        float centerFrequencyHz;
    };
    exception SignalSourceError {string msg; };

    interface WaveformBooter extends Frontend::AbstractReceiver {
        string  launchWaveform(string waveformClass, WaveformArgs       args)
                throws WaveformRunningError, SignalSourceError;

//        string  launchWaveformWithSession(string waveformClass, WaveformArgs       args, IceGrid::Session* session)
//                throws WaveformRunningError;
        WaveformArgMap getDriverEnum();
        WaveformArgMap getSourceInfo();
	idempotent bool	waveformRunning();
    	idempotent string  getWaveformClass();
        void    shutdown();
    };
};

//interface Pingable {
//	bool ping();
//};

};

#endif
