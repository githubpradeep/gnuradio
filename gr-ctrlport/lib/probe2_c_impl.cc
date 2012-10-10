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

#include "probe2_c_impl.h"
#include <gr_io_signature.h>

namespace gr {
  namespace ctrlport {

    probe2_c::sptr probe2_c::make(const std::string &id,
				  const std::string &desc, int len)
    {
      return gnuradio::get_initial_sptr(new probe2_c_impl(id, desc, len));
    }


    probe2_c_impl::probe2_c_impl(const std::string &id,
				 const std::string &desc, int len)
      : gr_sync_block("probe2_c",
		      gr_make_io_signature(1, 1, sizeof(gr_complex)),
		      gr_make_io_signature(0, 0, 0)),
	d_len(len),
	d_const_rpc(d_name, id.c_str(), this, unique_id(), &probe2_c::get,
		    pmt::pmt_make_c32vector(0,-2),
		    pmt::pmt_make_c32vector(0,2),
		    pmt::pmt_make_c32vector(0,0), 
		    "volts", desc.c_str(), RPC_PRIVLVL_MIN, DISPXYSCATTER),
	d_len_get_rpc(d_name, "length", this, unique_id(), &probe2_c::length,
		      pmt::mp(1), pmt::mp(10*len), pmt::mp(len),
		      "samples", "get vector length", RPC_PRIVLVL_MIN, DISPNULL),
	d_len_set_rpc(d_name, "length", this, unique_id(), &probe2_c::set_length,
		      pmt::mp(1), pmt::mp(10*len), pmt::mp(len),
		      "samples", "set vector length", RPC_PRIVLVL_MIN, DISPNULL)
    {
      set_length(len);
    }


    probe2_c_impl::~probe2_c_impl()
    {
    }

    //    boost::shared_mutex mutex_buffer;
    //    mutable boost::mutex mutex_notify;
    //    boost::condition_variable condition_buffer_ready;

    std::vector<gr_complex>
    probe2_c_impl::get()
    {
      mutex_buffer.lock();
      d_buffer.clear();
      mutex_buffer.unlock();

      // wait for condition
      boost::mutex::scoped_lock lock(mutex_notify);
      condition_buffer_ready.wait(lock);

      mutex_buffer.lock();
      std::vector<gr_complex> buf_copy = d_buffer;
      //d_buffer.clear();
      assert(buf_copy.size() == d_len);
      mutex_buffer.unlock();

      return buf_copy;
    }

    void
    probe2_c_impl::set_length(int len)
    {
      d_len = len;
      d_buffer.reserve(d_len);
    }

    int
    probe2_c_impl::length() const
    {
      return (int)d_len;
    }

    int
    probe2_c_impl::work(int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex*)input_items[0];

      // copy samples to get buffer if we need samples
      mutex_buffer.lock();
      if(d_buffer.size() < d_len) {
	// copy smaller of remaining buffer space and num inputs to work()
	int num_copy = std::min( (int)(d_len - d_buffer.size()), noutput_items );

	// TODO: convert this to a copy operator for speed...
	for(int i = 0; i < num_copy; i++) {
	  d_buffer.push_back(in[i]);
	}
    
	// notify the waiting get() if we fill up the buffer
	if(d_buffer.size() == d_len) {
	  condition_buffer_ready.notify_one();
	}
      }
      mutex_buffer.unlock();
    
      return noutput_items;
    }

  } /* namespace ctrlport */
} /* namespace gr */