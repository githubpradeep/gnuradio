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

#include "channel_model_impl.h"
#include <gr_io_signature.h>
#include <iostream>

namespace gr {
  namespace filter {
    
    channel_model::sptr
    channel_model::make(double noise_voltage,
			double frequency_offset,
			double epsilon,
			const std::vector<gr_complex> &taps,
			double noise_seed)
    {
      return gnuradio::get_initial_sptr
	(new channel_model_impl(noise_voltage,
				frequency_offset,
				epsilon,
				taps,
				noise_seed));
    }

    // Hierarchical block constructor
    channel_model_impl::channel_model_impl(double noise_voltage,
					   double frequency_offset,
					   double epsilon,
					   const std::vector<gr_complex> &taps,
					   double noise_seed)
      : gr_hier_block2("channel_model",
		       gr_make_io_signature(1, 1, sizeof(gr_complex)),
		       gr_make_io_signature(1, 1, sizeof(gr_complex)))
    {
      setup_rpc();

      d_taps = taps;
      while(d_taps.size() < 2) {
	d_taps.push_back(0);
      }

      d_timing_offset = fractional_interpolator_cc::make(0, epsilon);

      d_multipath = fir_filter_ccc::make(1, d_taps);

      d_noise_adder = gr_make_add_cc();
      d_noise = gr_make_noise_source_c(GR_GAUSSIAN, noise_voltage, noise_seed);
      d_freq_offset = gr_make_sig_source_c(1, GR_SIN_WAVE, frequency_offset, 1.0, 0.0);
      d_mixer_offset = gr_make_multiply_cc();

      connect(self(), 0, d_timing_offset, 0);
      connect(d_timing_offset, 0, d_multipath, 0);
      connect(d_multipath, 0, d_mixer_offset, 0);
      connect(d_freq_offset, 0, d_mixer_offset, 1);
      connect(d_mixer_offset, 0, d_noise_adder, 1);
      connect(d_noise, 0, d_noise_adder, 0);
      connect(d_noise_adder, 0, self(), 0);
    }

    channel_model_impl::~channel_model_impl()
    {
      takedown_rpc();
    }

    void
    channel_model_impl::set_noise_voltage(double noise_voltage)
    {
      d_noise->set_amplitude(noise_voltage);
    }

    void
    channel_model_impl::set_frequency_offset(double frequency_offset)
    {
      d_freq_offset->set_frequency(frequency_offset);
    }

    void
    channel_model_impl::set_taps(const std::vector<gr_complex> &taps)
    {
      d_taps = taps;
      while(d_taps.size() < 2) {
	d_taps.push_back(0);
      }
      d_multipath->set_taps(d_taps);
    }

    void
    channel_model_impl::set_timing_offset(double epsilon)
    {
      d_timing_offset->set_interp_ratio(epsilon);
    }

    double
    channel_model_impl::noise_voltage() const
    {
      return d_noise->amplitude();
    }

    double
    channel_model_impl::frequency_offset() const
    {
      return d_freq_offset->frequency();
    }

    std::vector<gr_complex>
    channel_model_impl::taps() const
    {
      return d_multipath->taps();
    }

    double
    channel_model_impl::timing_offset() const
    {
      return d_timing_offset->interp_ratio();
    }

#ifdef ENABLE_GR_CTRLPORT
    void
    channel_model_impl::setup_rpc()
    {
      d_noise_get = new rpcbasic_register_get<channel_model_impl, double>
	(d_name, "noise", this, unique_id(),
	 &channel_model_impl::noise_voltage,
	 pmt::mp(-10.0f), pmt::mp(10.0f), pmt::mp(0.0f),
	 "", "Noise Voltage",
	 RPC_PRIVLVL_MIN, DISPTIMESERIESF);

      d_freq_get = new rpcbasic_register_get<channel_model_impl, double>
	(d_name, "freq", this, unique_id(),
	 &channel_model_impl::frequency_offset,
	 pmt::mp(-1.0f), pmt::mp(1.0f), pmt::mp(0.0f),
	 "Hz", "Frequency Offset",
	 RPC_PRIVLVL_MIN, DISPTIMESERIESF);

      d_timing_get = new rpcbasic_register_get<channel_model_impl, double>
	(d_name, "timing", this, unique_id(),
	 &channel_model_impl::timing_offset,
	 pmt::mp(0.0f), pmt::mp(2.0f), pmt::mp(0.0f),
	 "", "Timing Offset",
	 RPC_PRIVLVL_MIN, DISPTIMESERIESF);

      d_taps_get = new rpcbasic_register_get<channel_model_impl, std::vector<gr_complex> >
	(d_name, "taps", this, unique_id(),
	 &channel_model_impl::taps,
	 pmt::pmt_make_c32vector(0,-10),
	 pmt::pmt_make_c32vector(0,10),
	 pmt::pmt_make_c32vector(0,0),
	 "", "Multipath taps",
	 RPC_PRIVLVL_MIN, DISPTIMESERIESF);

      d_noise_set = new rpcbasic_register_set<channel_model_impl, double>
	(d_name, "noise", this, unique_id(),
	 &channel_model_impl::set_noise_voltage,
	 pmt::mp(-10.0f), pmt::mp(10.0f), pmt::mp(0.0f),
	 "V", "Noise Voltage",
	 RPC_PRIVLVL_MIN, DISPNULL);

      d_freq_set = new rpcbasic_register_set<channel_model_impl, double>
	(d_name, "freq", this, unique_id(),
	 &channel_model_impl::set_frequency_offset,
	 pmt::mp(-1.0f), pmt::mp(1.0f), pmt::mp(0.0f),
	 "Hz", "Frequency Offset",
	 RPC_PRIVLVL_MIN, DISPNULL);

      d_timing_set = new rpcbasic_register_set<channel_model_impl, double>
	(d_name, "timing", this, unique_id(),
	 &channel_model_impl::set_timing_offset,
	 pmt::mp(0.0f), pmt::mp(2.0f), pmt::mp(0.0f),
	 "", "Timing Offset",
	 RPC_PRIVLVL_MIN, DISPNULL);

      /*
      d_taps_set = new rpcbasic_register_set<channel_model_impl, const std::vector<gr_complex>&>
	(d_name, "taps", this, unique_id(),
	 &channel_model_impl::set_taps,
	 pmt::pmt_make_c32vector(0,0),
	 pmt::pmt_make_c32vector(0,0),
	 pmt::pmt_make_c32vector(0,0),
	 "", "Multipath taps",
	 RPC_PRIVLVL_MIN, DISPTIMESERIESF);
      */
    }

    void
    channel_model_impl::takedown_rpc()
    {
      delete d_noise_get; 
      delete d_freq_get;  
      delete d_timing_get;
      delete d_taps_get;
      delete d_noise_set; 
      delete d_freq_set;  
      delete d_timing_set;
    }
#endif /* ENABLE_GR_CTRLPORT */

  } /* namespace filter */
} /* namespace gr */
