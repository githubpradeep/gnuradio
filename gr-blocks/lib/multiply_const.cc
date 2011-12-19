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

#include <gnuradio/blocks/multiply_const.h>
#include <gr_io_signature.h>
#include <stdexcept>
#include <complex>
#include <volk/volk.h>

using namespace gnuradio::blocks;

/***********************************************************************
 * Helper routines for conversion
 **********************************************************************/
template <typename type> void conv(const std::complex<double> &in, std::complex<type> &out){
    out = std::complex<type>(in);
}

template <typename type> void conv(const std::complex<double> &in, type &out){
    out = type(in.real());
}

/***********************************************************************
 * FC32 multiply const implementation
 **********************************************************************/
class multiply_const_fc32 : public multiply_const{
public:
    typedef std::complex<float> type;

    multiply_const_fc32(void):
        gr_sync_block(
            "multiply const fc32",
            gr_make_io_signature (1, 1, sizeof(type)),
            gr_make_io_signature (1, 1, sizeof(type))
        )
    {
        d_val.resize(1);
        const int alignment_multiple = volk_get_alignment() / (sizeof(type));
        set_output_multiple(std::max(1, alignment_multiple));
    }

    int work(
        int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        const type scalar = d_val[0];
        type *out = reinterpret_cast<type *>(output_items[0]);
        const type *in = reinterpret_cast<const type *>(input_items[0]);
        volk_32fc_s32fc_multiply_32fc_a(out, in, scalar, noutput_items);
        return noutput_items;
    }

    void _set_value(const std::vector<std::complex<double> > &val){
        if (val.size() != d_val.size()){
            throw std::invalid_argument("set_value called with the wrong length");
        }
        for (size_t i = 0; i < val.size(); i++){
            conv(val[i], d_val[i]);
        }
    }

protected:
    std::vector<type> d_val;
};

/***********************************************************************
 * FC32 multiply const implementation
 **********************************************************************/
class multiply_const_f32 : public multiply_const{
public:
    typedef float type;

    multiply_const_f32(void):
        gr_sync_block(
            "multiply const f32",
            gr_make_io_signature (1, 1, sizeof(type)),
            gr_make_io_signature (1, 1, sizeof(type))
        )
    {
        d_val.resize(1);
        const int alignment_multiple = volk_get_alignment() / sizeof(type);
        set_output_multiple(std::max(1, alignment_multiple));
    }

    int work(
        int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        const type scalar = d_val[0];
        type *out = reinterpret_cast<type *>(output_items[0]);
        const type *in = reinterpret_cast<const type *>(input_items[0]);
        volk_32f_s32f_multiply_32f_a(out, in, scalar, noutput_items);
        return noutput_items;
    }

    void _set_value(const std::vector<std::complex<double> > &val){
        if (val.size() != d_val.size()){
            throw std::invalid_argument("set_value called with the wrong length");
        }
        for (size_t i = 0; i < val.size(); i++){
            conv(val[i], d_val[i]);
        }
    }

protected:
    std::vector<type> d_val;
};

/***********************************************************************
 * Generic multiply const implementation
 **********************************************************************/
template <typename type>
class multiply_const_generic : public multiply_const{
public:
    multiply_const_generic(const size_t vlen):
        gr_sync_block(
            "multiply const generic",
            gr_make_io_signature (1, 1, sizeof(type)*vlen),
            gr_make_io_signature (1, 1, sizeof(type)*vlen)
        )
    {
        d_val.resize(vlen);
    }

    int work(
        int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        const size_t n_nums = noutput_items * d_val.size();
        type *out = reinterpret_cast<type *>(output_items[0]);
        const type *in = reinterpret_cast<const type *>(input_items[0]);

        //simple vec len 1 for the fast
        if (d_val.size() == 1){
            const type val = d_val[0];
            for (size_t i = 0; i < n_nums; i++){
                out[i] = in[i] * val;
            }
        }

        //general case for any vlen
        else{
            for (size_t i = 0; i < n_nums; i++){
                out[i] = in[i] * d_val[i%d_val.size()];
            }
        }
        return noutput_items;
    }

    void _set_value(const std::vector<std::complex<double> > &val){
        if (val.size() != d_val.size()){
            throw std::invalid_argument("set_value called with the wrong length");
        }
        for (size_t i = 0; i < val.size(); i++){
            conv(val[i], d_val[i]);
        }
    }

protected:
    std::vector<type> d_val;
};

/***********************************************************************
 * factory function
 **********************************************************************/
multiply_const::sptr multiply_const::make(op_type type, const size_t vlen){

    if (type == OP_FC32 && vlen == 1) return sptr(new multiply_const_fc32());
    if (type == OP_F32 && vlen == 1) return sptr(new multiply_const_f32());

    switch(type){
    case OP_FC64: return sptr(new multiply_const_generic<std::complex<double> >(vlen));
    case OP_F64: return sptr(new multiply_const_generic<double>(vlen));

    case OP_FC32: return sptr(new multiply_const_generic<std::complex<float> >(vlen));
    case OP_F32: return sptr(new multiply_const_generic<float>(vlen));

    case OP_SC64: return sptr(new multiply_const_generic<std::complex<int64_t> >(vlen));
    case OP_S64: return sptr(new multiply_const_generic<int64_t>(vlen));

    case OP_SC32: return sptr(new multiply_const_generic<std::complex<int32_t> >(vlen));
    case OP_S32: return sptr(new multiply_const_generic<int32_t>(vlen));

    case OP_SC16: return sptr(new multiply_const_generic<std::complex<int16_t> >(vlen));
    case OP_S16: return sptr(new multiply_const_generic<int16_t>(vlen));

    case OP_SC8: return sptr(new multiply_const_generic<std::complex<int8_t> >(vlen));
    case OP_S8: return sptr(new multiply_const_generic<int8_t>(vlen));

    default: throw std::invalid_argument("make multiply const got unknown type");
    }
}

