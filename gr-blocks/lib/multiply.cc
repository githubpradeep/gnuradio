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

#include <gnuradio/blocks/multiply.h>
#include <gr_io_signature.h>
#include <stdexcept>
#include <complex>
#include <volk/volk.h>

using namespace gnuradio::blocks;

/***********************************************************************
 * Multiplier implementation with complex float32 - calls volk
 **********************************************************************/
class multiply_fc32 : public multiply{
public:
    multiply_fc32(const size_t vlen):
        gr_sync_block(
            "multiply fc32",
            gr_make_io_signature (1, -1, sizeof(std::complex<float>)*vlen),
            gr_make_io_signature (1, 1, sizeof(std::complex<float>)*vlen)
        ),
        d_vlen(vlen)
    {
        const int alignment_multiple = volk_get_alignment() / (sizeof(std::complex<float>)*vlen);
        set_output_multiple(std::max(1, alignment_multiple));
    }

    int work(
        int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        const size_t n_nums = noutput_items * d_vlen;
        std::complex<float> *out = reinterpret_cast<std::complex<float> *>(output_items[0]);
        const std::complex<float> *in0 = reinterpret_cast<const std::complex<float> *>(input_items[0]);

        for (size_t n = 1; n < input_items.size(); n++){
            const std::complex<float> *in = reinterpret_cast<const std::complex<float> *>(input_items[n]);
            volk_32fc_x2_multiply_32fc_a(out, in0, in, n_nums);
            in0 = out; //for next input, we do output += input
        }

        return noutput_items;
    }

private:
    const size_t d_vlen;
};

/***********************************************************************
 * Multiplier implementation with float32 - calls volk
 **********************************************************************/
class multiply_f32 : public multiply{
public:
    multiply_f32(const size_t vlen):
        gr_sync_block(
            "multiply f32",
            gr_make_io_signature (1, -1, sizeof(float)*vlen),
            gr_make_io_signature (1, 1, sizeof(float)*vlen)
        ),
        d_vlen(vlen)
    {
        const int alignment_multiple = volk_get_alignment() / (sizeof(float)*vlen);
        set_output_multiple(std::max(1, alignment_multiple));
    }

    int work(
        int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        const size_t n_nums = noutput_items * d_vlen;
        float *out = reinterpret_cast<float *>(output_items[0]);
        const float *in0 = reinterpret_cast<const float *>(input_items[0]);

        for (size_t n = 1; n < input_items.size(); n++){
            const float *in = reinterpret_cast<const float *>(input_items[n]);
            volk_32f_x2_multiply_32f_a(out, in0, in, n_nums);
            in0 = out; //for next input, we do output += input
        }

        return noutput_items;
    }

private:
    const size_t d_vlen;
};

/***********************************************************************
 * Generic multiplyer implementation
 **********************************************************************/
template <typename type>
class multiply_generic : public multiply{
public:
    multiply_generic(const size_t vlen):
        gr_sync_block(
            "multiply generic",
            gr_make_io_signature (1, -1, sizeof(type)*vlen),
            gr_make_io_signature (1, 1, sizeof(type)*vlen)
        ),
        d_vlen(vlen)
    {
        //NOP
    }

    int work(
        int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        const size_t n_nums = noutput_items * d_vlen;
        type *out = reinterpret_cast<type *>(output_items[0]);
        const type *in0 = reinterpret_cast<const type *>(input_items[0]);

        for (size_t n = 1; n < input_items.size(); n++){
            const type *in = reinterpret_cast<const type *>(input_items[n]);
            for (size_t i = 0; i < n_nums; i++){
                out[i] = in0[i] * in[i];
            }
            in0 = out; //for next input, we do output *= input
        }

        return noutput_items;
    }

private:
    const size_t d_vlen;
};

/***********************************************************************
 * factory function
 **********************************************************************/
multiply::sptr multiply::make(op_type type, const size_t vlen){
    switch(type){
    case OP_FC64: return sptr(new multiply_generic<std::complex<double> >(vlen));
    case OP_F64: return sptr(new multiply_generic<double>(vlen));

    case OP_FC32: return sptr(new multiply_fc32(vlen));
    case OP_F32: return sptr(new multiply_f32(vlen));

    case OP_SC64: return sptr(new multiply_generic<std::complex<int64_t> >(vlen));
    case OP_S64: return sptr(new multiply_generic<int64_t>(vlen));

    case OP_SC32: return sptr(new multiply_generic<std::complex<int32_t> >(vlen));
    case OP_S32: return sptr(new multiply_generic<int32_t>(vlen));

    case OP_SC16: return sptr(new multiply_generic<std::complex<int16_t> >(vlen));
    case OP_S16: return sptr(new multiply_generic<int16_t>(vlen));

    case OP_SC8: return sptr(new multiply_generic<std::complex<int8_t> >(vlen));
    case OP_S8: return sptr(new multiply_generic<int8_t>(vlen));

    default: throw std::invalid_argument("make multiply got unknown type");
    }
}
