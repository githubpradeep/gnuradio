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

#ifndef INCLUDED_CTRLPORT_PROBE2_C_H
#define INCLUDED_CTRLPORT_PROBE2_C_H

#include <ctrlport/api.h>
#include <gr_sync_block.h>

namespace gr {
  namespace ctrlport {
    
    /*!
     * \brief A complex value probe to pass a pre-set length of data through ctrlport.
     *
     */
    class CTRLPORT_API probe2_c : virtual public gr_sync_block
    {
    public:
      // gr::ctrlport::probe2_c::sptr
      typedef boost::shared_ptr<probe2_c> sptr;

      /*!
       * Build a complex value control port probe with fixed length.
       *
       * \param id name to give to the probe.
       * \param desc string describing what the probe is for.
       * \param len the lnegth of the vector to pass.
       */
      static sptr make(const std::string &id, const std::string &desc, int len);

      virtual std::vector<gr_complex> get() = 0;
      virtual void set_length(int len) = 0;
      virtual int length() const = 0;
    };

  } /* namespace ctrlport */
} /* namespace gr */

#endif /* INCLUDED_CTRLPORT_PROBE2_C_H */

