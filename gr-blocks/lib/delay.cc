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

#include <gnuradio/blocks/delay.h>
#include <gr_io_signature.h>
#include <cstring> //memcpy
#include <gruel/thread.h>

using namespace gnuradio::blocks;

/***********************************************************************
 * Generic delay implementation
 **********************************************************************/
class delay_impl : public delay{
public:
    delay_impl(const size_t itemsize):
        gr_block(
            "blocks delay block",
            gr_make_io_signature (1, 1, itemsize),
            gr_make_io_signature (1, 1, itemsize)
        ),
        d_itemsize(itemsize)
    {
        this->set_delay(0);
    }

    void set_delay(const int nitems){
        gruel::scoped_lock l(d_delay_mutex);
        d_delay_items = nitems;
    }

    int general_work(
        int noutput_items,
        gr_vector_int &ninput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        gruel::scoped_lock l(d_delay_mutex);
        const int delta = int64_t(nitems_read(0)) \
	  - int64_t(nitems_written(0)) - d_delay_items;

        //consume but not produce (drops samples)
        if (delta < 0){
            consume_each(std::min(ninput_items[0], -delta));
            return 0;
        }

        //produce but not consume (inserts zeros)
        if (delta > 0){
            noutput_items = std::min(noutput_items, delta);
            std::memset(output_items[0], 0, noutput_items*d_itemsize);
            return noutput_items;
        }

        //otherwise just memcpy
        noutput_items = std::min(noutput_items, ninput_items[0]);
        std::memcpy(output_items[0], input_items[0], noutput_items*d_itemsize);
        consume_each(noutput_items);
        return noutput_items;
    }

private:
    int d_delay_items;
    const size_t d_itemsize;
    gruel::mutex d_delay_mutex;
};

/***********************************************************************
 * Delay factory function
 **********************************************************************/
delay::sptr delay::make(const size_t itemsize){
    return sptr(new delay_impl(itemsize));
}
