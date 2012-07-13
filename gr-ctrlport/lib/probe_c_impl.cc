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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "probe_c_impl.h"
#include <gr_io_signature.h>

namespace gr {
  namespace ctrlport {

    probe_c::sptr probe_c::make(const std::string &id,
				const std::string &desc)
    {
      return gnuradio::get_initial_sptr(new probe_c_impl(id, desc));
    }


    probe_c_impl::probe_c_impl(const std::string &id,
			       const std::string &desc)
      : gr_sync_block("probe_c",
		      gr_make_io_signature(1, 1, sizeof(gr_complex)),
		      gr_make_io_signature(0, 0, 0)),
	d_ptr(NULL), d_ptrLen(0),
	d_const_rpc(d_name, id.c_str(), this, unique_id(), &probe_c::get, 
		    pmt::pmt_make_c32vector(0,-2),
		    pmt::pmt_make_c32vector(0,2),
		    pmt::pmt_make_c32vector(0,0), 
		    "volts", desc.c_str(), RPC_PRIVLVL_MIN, DISPXYSCATTER)
    {
    }


    probe_c_impl::~probe_c_impl()
    {
    }

    std::vector<gr_complex>
    probe_c_impl::get()
    {
      if(d_ptr != NULL && d_ptrLen > 0) {
	ptrlock.lock();
	std::vector<gr_complex> vec(d_ptr, d_ptr+d_ptrLen);
	ptrlock.unlock();
	return vec;
      }
      else {
	std::vector<gr_complex> vec;
	return vec;
      }
    }

    int
    probe_c_impl::work(int noutput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex*)input_items[0];

      // keep reference to symbols
      ptrlock.lock();
      d_ptr = in;
      d_ptrLen = noutput_items;
      ptrlock.unlock();
    
      return noutput_items;
    }

  } /* namespace ctrlport */
} /* namespace gr */
