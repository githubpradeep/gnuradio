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
include $(top_srcdir)/Makefile.swig

TESTS =
EXTRA_DIST =

AM_CPPFLAGS = \
	$(GR_BLOCKS_INCLUDES) \
	$(STD_DEFINES_AND_INCLUDES) \
	$(PYTHON_CPPFLAGS) \
	$(WITH_INCLUDES)


##############################
# SWIG interface and library
TOP_SWIG_IFILES = \
	blocks_swig.i

# Install so that they end up available as:
#   import gnuradio.blocks
# This ends up at:
#   ${prefix}/lib/python${python_version}/site-packages/gnuradio/blocks
blocks_swig_pythondir_category = \
	gnuradio/blocks

# additional libraries for linking with the SWIG-generated library
blocks_swig_la_swig_libadd = \
	$(abs_top_builddir)/gr-blocks/lib/libgnuradio-blocks.la

# additional SWIG files to be installed
blocks_swig_swiginclude_headers =	\
	blocks_delay.i			\
	blocks_ops.i			\
	blocks_sources.i		\
	blocks_stream_selector.i

blocks_swig_swig_args = \
	$(GR_BLOCKS_INCLUDES)

# Turned GUILE off; even if --enable-guile, don't build
# anything; this overrides the automatic build rule.
if GUILE
gnuradio/%.scm: %.i
	echo "Not building guile."
endif