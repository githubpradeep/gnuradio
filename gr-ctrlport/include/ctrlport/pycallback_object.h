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

#include <iostream>
#include <ctrlport/rpcregisterhelpers.h>
#include <ctrlport/ice_application_base.h>
#include <ctrlport/IcePy_Communicator.h>
#include <pythread.h>

enum pyport_t {
  PYPORT_STRING,
  PYPORT_FLOAT
};

class Instance 
{
public:
  static boost::shared_ptr<ice_application_common> get_application()
  {
    return ice_application_common::Instance();
  }
  static Ice::CommunicatorPtr get_swig_communicator()
  {
    return get_application()->communicator();
  }
};

int pycallback_object_count = 500;

// a simple to-PMT converter template class-function
template <class myType> class pmt_assist
{
public:
  static pmt::pmt_t make(myType _val) 
  { 
    return pmt::mp(_val);
  }
};

/* template specializations for vectors that cant use pmt::mp() */
template<>
pmt::pmt_t pmt_assist<std::vector<float> >::make(std::vector<float> _val)
{
  return pmt::pmt_init_f32vector(_val.size(), &_val[0]);
}

template<>
pmt::pmt_t pmt_assist<std::vector<gr_complex> >::make(std::vector<gr_complex> _val)
{
  return pmt::pmt_init_c32vector(_val.size(), &_val[0]); 
}

template <class myType> class pycallback_object
{
public:
  pycallback_object(std::string name, std::string functionbase,
		    std::string units, std::string desc,
		    myType min, myType max, myType deflt,
		    display_type_t dtype) :
    d_callback(NULL),
    d_rpc(name, functionbase.c_str(), this, pycallback_object_count++,
	  &pycallback_object::get, pmt_assist<myType>::make(min),
	  pmt_assist<myType>::make(max),  pmt_assist<myType>::make(deflt),
	  units.c_str(), desc.c_str(), RPC_PRIVLVL_MIN, dtype)
    //pmt::mp(min), pmt::mp(max), pmt::mp(deflt), units.c_str(), desc.c_str(), RPC_PRIVLVL_MIN, dtype)
  {
    d_callback = NULL;
  }
    
  myType get() {
    myType rVal;
    if(d_callback == NULL) {
      printf("WARNING: pycallback_object get() called without py callback set!\n");
      return rVal;
    }
    else {
      // obtain  PyGIL
      PyGILState_STATE state = PyGILState_Ensure();

      PyObject *func;
      //PyObject *arglist;
      PyObject *result;
   
      func = (PyObject *) d_callback;               // Get Python function
      //arglist = Py_BuildValue("");             // Build argument list
      result = PyEval_CallObject(func,NULL);     // Call Python
      //result = PyEval_CallObject(func,arglist);     // Call Python
      //Py_DECREF(arglist);                           // Trash arglist
      if(result) {                                 // If no errors, return double
	rVal = pyCast(result);
      }
      Py_XDECREF(result);

      // release  PyGIL
      PyGILState_Release(state);
      //std::cout << "returning: " << rVal << std::endl;
      return rVal;
    }
  }
  
  void set_callback(PyObject *cb)
  {
    d_callback = cb;
  }
  
private:
  PyObject* d_callback;
  rpcbasic_register_get<pycallback_object, myType> d_rpc;

  myType pyCast(PyObject* obj) {
    printf("TYPE NOT IMPLEMENTED!\n");
    assert(0);
  };
};


// template specialization conversion functions
// get data out of the PyObject and into the real world
template<> 
std::string pycallback_object<std::string>::pyCast(PyObject* obj)
{
  return std::string(PyString_AsString(obj));
}

template<> 
double pycallback_object<double>::pyCast(PyObject* obj)
{
  return PyFloat_AsDouble(obj);
}

template<> 
float pycallback_object<float>::pyCast(PyObject* obj)
{
  return (float)PyFloat_AsDouble(obj);
}

template<> 
int pycallback_object<int>::pyCast(PyObject* obj)
{
  return PyInt_AsLong(obj);
}

template<> 
std::vector<float> pycallback_object<std::vector<float> >::pyCast(PyObject* obj)
{
  int size = PyObject_Size(obj);
  std::vector<float> rval(size);
  for(int i=0; i<size; i++) {
    rval[i] = (float)PyFloat_AsDouble(PyList_GetItem(obj, i));
  }
  return rval;
}

template<> 
std::vector<gr_complex> pycallback_object<std::vector<gr_complex> >::pyCast(PyObject* obj)
{
  int size = PyObject_Size(obj);
  std::vector<gr_complex> rval(size);
  for(int i=0; i<size; i++){ rval[i] = \
      gr_complex((float)PyComplex_RealAsDouble(PyList_GetItem(obj, i)),
		 (float)PyComplex_ImagAsDouble(PyList_GetItem(obj, i))); 
  }
  return rval;
}
// TODO: add more template specializations as needed!