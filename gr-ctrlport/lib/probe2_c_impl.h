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

#ifndef INCLUDED_CTRLPORT_PROBE2_C_IMPL_H
#define INCLUDED_CTRLPORT_PROBE2_C_IMPL_H

#include <ctrlport/probe2_c.h>
#include <ctrlport/rpcregisterhelpers.h>
#include <boost/thread/shared_mutex.hpp>

namespace gr {
  namespace ctrlport {

    class CTRLPORT_API probe2_c_impl : public probe2_c
    {
    private:
      size_t d_len;
      boost::shared_mutex mutex_buffer;
      mutable boost::mutex mutex_notify;
      boost::condition_variable condition_buffer_ready;

      std::vector<gr_complex> d_buffer;

      rpcbasic_register_get<probe2_c_impl, std::vector<std::complex<float> >  > d_const_rpc;
      rpcbasic_register_get<probe2_c_impl, int> d_len_get_rpc;
      rpcbasic_register_set<probe2_c_impl, int> d_len_set_rpc;

    public:
      probe2_c_impl(const std::string &id, const std::string &desc, int len);
      ~probe2_c_impl();

      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      std::vector<gr_complex> get();

      void set_length(int len);
      int length() const;

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } /* namespace ctrlport */
} /* namespace gr */

#endif /* INCLUDED_CTRLPORT_PROBE2_C_IMPL_H */

