/* -*- c++ -*- */
/*
 * Copyright 2008 Free Software Foundation, Inc.
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

#include <usrp2_source_base.h>
#include <gr_io_signature.h>
#include <iostream>

#define USRP2_SOURCE_BASE_DEBUG 0

usrp2_source_base::usrp2_source_base(const char *name,
				     gr_io_signature_sptr output_signature,
				     const std::string &ifc,
				     const std::string &mac) 
  throw (std::runtime_error)
  : gr_sync_block(name,
		  gr_make_io_signature(0, 0, 0),
		  output_signature),
    d_u2(usrp2::usrp2::sptr())
{
  d_u2 = usrp2::usrp2::make(ifc, mac);
  if (!d_u2)
    throw std::runtime_error("Unable to initialize USRP2!");
}

usrp2_source_base::~usrp2_source_base ()
{
}

bool
usrp2_source_base::set_gain(double gain)
{
  return d_u2->set_rx_gain(gain);
}

bool
usrp2_source_base::set_center_freq(double frequency, usrp2::tune_result *tr)
{
  return d_u2->set_rx_center_freq(frequency, tr);
}

bool
usrp2_source_base::set_decim(int decimation_factor)
{
  return d_u2->set_rx_decim(decimation_factor);
}

std::string
usrp2_source_base::mac_addr()
{
  return d_u2->mac_addr();
}

bool
usrp2_source_base::start()
{
  if (USRP2_SOURCE_BASE_DEBUG)
    printf("usrp2_source_base::start()\n");

  return d_u2->start_rx_streaming(0); // FIXME: someday sources will have channel #s
}

bool
usrp2_source_base::stop()
{
  if (USRP2_SOURCE_BASE_DEBUG)
    printf("usrp2_source_base::stop()\n");

  return d_u2->stop_rx_streaming(0); // FIXME: someday sources will have channel #s
}