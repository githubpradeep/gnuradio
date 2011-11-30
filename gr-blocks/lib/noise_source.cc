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

#include <gnuradio/blocks/noise_source.h>
#include <gr_io_signature.h>
#include <gr_random.h>
#include <stdexcept>
#include <complex>
#include <cmath>
#include <boost/math/special_functions/round.hpp>

using namespace gnuradio::blocks;

static const size_t wave_table_size = 4096;

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
 * Generic add const implementation
 **********************************************************************/
template <typename type>
class noise_source_impl : public noise_source{
public:
    noise_source_impl(const long seed):
        gr_sync_block(
            "noise source",
            gr_make_io_signature (0, 0, 0),
            gr_make_io_signature (1, 1, sizeof(type))
        ),
        _index(0),
        _table(wave_table_size),
        _offset(0.0), _scaler(1.0),
        _wave("GAUSSIAN"),
        _random(seed)
    {
        this->update_table();
    }

    int work(
        int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items
    ){
        type *out = reinterpret_cast<type *>(output_items[0]);
        for (size_t i = 0; i < size_t(noutput_items); i++){
            out[i] = _table[_index % wave_table_size];
            _index++;
        }
        return noutput_items;
    }

    void set_waveform(const std::string &wave){
        _wave = wave;
        this->update_table();
    }

    void set_offset(const std::complex<double> &offset){
        _offset = offset;
        this->update_table();
    }

    void set_scaler(const std::complex<double> &scaler){
        _scaler = scaler;
        this->update_table();
    }

    void update_table(void){
        if (_wave == "UNIFORM"){
            for (size_t i = 0; i < _table.size(); i++){
                this->set_elem(i, std::complex<double>(2*_random.ran1()-1, 2*_random.ran1()-1));
            }
        }
        else if (_wave == "GAUSSIAN"){
            for (size_t i = 0; i < _table.size(); i++){
                this->set_elem(i, std::complex<double>(_random.gasdev(), _random.gasdev()));
            }
        }
        else if (_wave == "LAPLACIAN"){
            for (size_t i = 0; i < _table.size(); i++){
                this->set_elem(i, std::complex<double>(_random.laplacian(), _random.laplacian()));
            }
        }
        else if (_wave == "IMPULSE"){
            const float factor = 9; //TODO pass as param
            for (size_t i = 0; i < _table.size(); i++){
                this->set_elem(i, std::complex<double>(_random.impulse(factor), _random.impulse(factor)));
            }
        }
        else throw std::invalid_argument("noise source got unknown wave type: " + _wave);
    }

    inline void set_elem(const size_t index, const std::complex<double> &val){
        conv(_scaler * val + _offset, _table[index]);
    }

private:
    size_t _index;
    std::vector<type> _table;
    std::complex<double> _offset, _scaler;
    std::string _wave;
    gr_random _random;
};

/***********************************************************************
 * Adder factory function
 **********************************************************************/
noise_source::sptr noise_source::make(op_type type, const long seed){
    switch(type){
    case OP_FC64: return sptr(new noise_source_impl<std::complex<double> >(seed));
    case OP_F64: return sptr(new noise_source_impl<double>(seed));

    case OP_FC32: return sptr(new noise_source_impl<std::complex<float> >(seed));
    case OP_F32: return sptr(new noise_source_impl<float>(seed));

    case OP_SC64: return sptr(new noise_source_impl<std::complex<int64_t> >(seed));
    case OP_S64: return sptr(new noise_source_impl<int64_t>(seed));

    case OP_SC32: return sptr(new noise_source_impl<std::complex<int32_t> >(seed));
    case OP_S32: return sptr(new noise_source_impl<int32_t>(seed));

    case OP_SC16: return sptr(new noise_source_impl<std::complex<int16_t> >(seed));
    case OP_S16: return sptr(new noise_source_impl<int16_t>(seed));

    case OP_SC8: return sptr(new noise_source_impl<std::complex<int8_t> >(seed));
    case OP_S8: return sptr(new noise_source_impl<int8_t>(seed));

    default: throw std::invalid_argument("make noise source got unknown type");
    }
}
