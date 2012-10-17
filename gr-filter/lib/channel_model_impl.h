/* -*- c++ -*- */
/*
 * Copyright 2009,2012 Free Software Foundation, Inc.
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

#ifndef INCLUDED_FILTER_CHANNEL_MODEL_IMPL_H
#define INCLUDED_FILTER_CHANNEL_MODEL_IMPL_H

#include <gr_top_block.h>
#include <gr_sig_source_c.h>
#include <gr_add_cc.h>
#include <gr_multiply_cc.h>
#include <gr_noise_source_c.h>
#include <filter/channel_model.h>
#include <filter/fractional_interpolator_cc.h>
#include <filter/fir_filter_ccc.h>

#ifdef ENABLE_GR_CTRLPORT
#include <ctrlport/rpcregisterhelpers.h>
#endif

namespace gr {
  namespace filter {

    class FILTER_API channel_model_impl : public channel_model
    {
    private:
      gr_sig_source_c_sptr d_freq_offset;
      gr_add_cc_sptr d_noise_adder;
      gr_noise_source_c_sptr d_noise;
      gr_multiply_cc_sptr d_mixer_offset;

      fractional_interpolator_cc::sptr d_timing_offset;
      fir_filter_ccc::sptr d_multipath;

      std::vector<gr_complex> d_taps;

#ifdef ENABLE_GR_CTRLPORT
      typedef rpcbasic_register_get<channel_model_impl, double> get_64f_t;
      typedef rpcbasic_register_set<channel_model_impl, double> set_64f_t;
      typedef rpcbasic_register_get<channel_model_impl, std::vector<gr_complex> > get_v32fc_t;
      typedef rpcbasic_register_set<channel_model_impl, std::vector<gr_complex> > set_v32fc_t;
      typedef boost::shared_ptr<get_64f_t> get_64f_sptr;
      typedef boost::shared_ptr<set_64f_t> set_64f_sptr;
      typedef boost::shared_ptr<get_v32fc_t> get_v32fc_sptr;
      typedef boost::shared_ptr<set_v32fc_t> set_v32fc_sptr;

      std::vector<get_64f_sptr> d_get_64f_rpcs;
      std::vector<set_64f_sptr> d_set_64f_rpcs;

      std::vector<get_v32fc_sptr> d_get_v32fc_rpcs;
      //std::vector<set_32fc_sptr> d_set_v32fc_rpcs;
#endif /* ENABLE_GR_CTRLPORT */

      void setup_rpc();

    public:
      channel_model_impl(double noise_voltage,
			 double frequency_offset,
			 double epsilon,
			 const std::vector<gr_complex> &taps,
			 double noise_seed);
      
      ~channel_model_impl();

      void set_noise_voltage(double noise_voltage);
      void set_frequency_offset(double frequency_offset);
      void set_taps(const std::vector<gr_complex> &taps);
      void set_timing_offset(double epsilon);

      double noise_voltage() const;
      double frequency_offset() const;
      std::vector<gr_complex> taps() const;
      double timing_offset() const;
    };

  } /* namespace filter */
} /* namespace gr */

#endif /* INCLUDED_FILTER_CHANNEL_MODEL_IMPL_H */
