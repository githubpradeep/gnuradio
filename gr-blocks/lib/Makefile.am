#
# Copyright 2011 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

include $(top_srcdir)/Makefile.common

AM_CPPFLAGS = $(STD_DEFINES_AND_INCLUDES) $(PYTHON_CPPFLAGS) \
	$(GR_BLOCKS_INCLUDES) $(WITH_INCLUDES)

lib_LTLIBRARIES = libgnuradio-blocks.la

libgnuradio_blocks_la_SOURCES = \
	add.cc			\
	add_const.cc		\
	delay.cc		\
	divide.cc		\
	multiply.cc		\
	multiply_const.cc	\
	noise_source.cc		\
	signal_source.cc	\
	stream_selector.cc	\
	subtract.cc


libgnuradio_blocks_la_LIBADD =	\
	$(GNURADIO_CORE_LA)

libgnuradio_blocks_la_LDFLAGS = $(NO_UNDEFINED) $(LTVERSIONFLAGS)
