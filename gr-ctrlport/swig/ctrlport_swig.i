/* -*- c++ -*- */
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

#define CTRLPORT_API

%include "gnuradio.i"

//load generated python docstrings
%include "ctrlport_swig_doc.i"

%template(StrVector) std::vector<std::string>;

%{
#include "ctrlport/rpcmanager.h"
#include "ctrlport/rpcserver_booter_base.h"
#include "ctrlport/rpcserver_booter_aggregator.h"
#include "ctrlport/probe_c.h"
#include "ctrlport/probe2_c.h"
%}

%include "ctrlport/rpcmanager.h"
%include "ctrlport/rpcserver_booter_base.h"
%include "ctrlport/rpcserver_booter_aggregator.h"
%include "ctrlport/probe_c.h"
%include "ctrlport/probe2_c.h"


GR_SWIG_BLOCK_MAGIC2(ctrlport, probe_c);
GR_SWIG_BLOCK_MAGIC2(ctrlport, probe2_c);

%{
#include <ctrlport/pycallback_object.h>
#include <ctrlport/rpccallbackregister_base.h>
%}

%include <ctrlport/pycallback_object.h>
%include <ctrlport/rpccallbackregister_base.h>

// Attach a new python callback method to Python function
%extend pycallback_object {
  // Set a Python function object as a callback function
  // Note : PyObject *pyfunc is remapped with a typempap
  void activate(PyObject *pyfunc)
  {
    self->set_callback( pyfunc );
    Py_INCREF(pyfunc);
  }
}

// this method appears to be broken and only valid for communicators created via the IcePy interface
%extend Instance {
  static PyObject* get_communicator()
  {
    return IcePy::getCommunicatorWrapper(Instance::get_swig_communicator());
  }
}

%template(RPC_get_string)   pycallback_object<std::string>;
%template(RPC_get_int)      pycallback_object<int>;
%template(RPC_get_float)    pycallback_object<float>;
%template(RPC_get_double)   pycallback_object<double>;
%template(RPC_get_vector_float)    pycallback_object<std::vector<float> >;
%template(RPC_get_vector_gr_complex)    pycallback_object<std::vector<gr_complex> >;
