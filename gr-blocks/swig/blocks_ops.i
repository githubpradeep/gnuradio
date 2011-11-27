/*
 * Copyright 2011 Free Software Foundation, Inc.
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

////////////////////////////////////////////////////////////////////////
// block headers
////////////////////////////////////////////////////////////////////////
%{
#include <gnuradio/blocks/add.h>
#include <gnuradio/blocks/add_const.h>
#include <gnuradio/blocks/divide.h>
#include <gnuradio/blocks/multiply.h>
#include <gnuradio/blocks/multiply_const.h>
#include <gnuradio/blocks/subtract.h>
%}

%include <gnuradio/blocks/add.h>
%include <gnuradio/blocks/add_const.h>
%include <gnuradio/blocks/divide.h>
%include <gnuradio/blocks/multiply.h>
%include <gnuradio/blocks/multiply_const.h>
%include <gnuradio/blocks/subtract.h>

////////////////////////////////////////////////////////////////////////
// template foo
////////////////////////////////////////////////////////////////////////
%template(set_value) gnuradio::blocks::add_const::set_value<std::complex<double> >;
%template(set_value) gnuradio::blocks::multiply_const::set_value<std::complex<double> >;

////////////////////////////////////////////////////////////////////////
// block magic
////////////////////////////////////////////////////////////////////////
using namespace gnuradio::blocks;
GR_SWIG_BLOCK_MAGIC1(add)
GR_SWIG_BLOCK_MAGIC1(add_const)
GR_SWIG_BLOCK_MAGIC1(divide)
GR_SWIG_BLOCK_MAGIC1(multiply)
GR_SWIG_BLOCK_MAGIC1(multiply_const)
GR_SWIG_BLOCK_MAGIC1(subtract)
