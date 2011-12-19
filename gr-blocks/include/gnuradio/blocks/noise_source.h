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

#ifndef INCLUDED_GR_BLOCKS_NOISE_SOURCE_H
#define INCLUDED_GR_BLOCKS_NOISE_SOURCE_H

#include <gnuradio/blocks/api.h>
#include <gnuradio/blocks/op_types.h>
#include <gr_sync_block.h>
#include <complex>

namespace gnuradio{ namespace blocks{

/*!
 * \brief random number source
 * \ingroup source_blk
 */
class GR_BLOCKS_API noise_source : virtual public gr_sync_block{
public:
    typedef boost::shared_ptr<noise_source> sptr;

    //! Make a new noise source given data type
    static sptr make(op_type type, const long seed = 42);

    //! Set the waveform type (UNIFORM, GAUSSIAN, LAPLACIAN, IMPULSE)
    virtual void set_waveform(const std::string &) = 0;

    //! Set the offset, this is a free addition operation
    virtual void set_offset(const std::complex<double> &) = 0;

    //! Set the amplitude, this is a free multiply scalar operation
    virtual void set_amplitude(const std::complex<double> &) = 0;

    //! Set the factor, this is used for the IMPULSE waveform
    virtual void set_factor(const double &factor) = 0;

};

}}

#endif /* INCLUDED_GR_BLOCKS_NOISE_SOURCE_H */
