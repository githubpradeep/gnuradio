dnl Copyright 2011 Free Software Foundation, Inc.
dnl 
dnl This file is part of GNU Radio
dnl 
dnl GNU Radio is free software; you can redistribute it and/or modify
dnl it under the terms of the GNU General Public License as published by
dnl the Free Software Foundation; either version 3, or (at your option)
dnl any later version.
dnl 
dnl GNU Radio is distributed in the hope that it will be useful,
dnl but WITHOUT ANY WARRANTY; without even the implied warranty of
dnl MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
dnl GNU General Public License for more details.
dnl 
dnl You should have received a copy of the GNU General Public License
dnl along with GNU Radio; see the file COPYING.  If not, write to
dnl the Free Software Foundation, Inc., 51 Franklin Street,
dnl Boston, MA 02110-1301, USA.

AC_DEFUN([GRC_GR_BLOCKS],[
    GRC_ENABLE(gr-blocks)

    dnl Don't do gr-blocks if gnuradio-core skipped
    GRC_CHECK_DEPENDENCY(gr-blocks, gnuradio-core)

    if test $passed != with && test x$enable_volk != xno; then
	dnl how and where to find INCLUDES and LA and such
        gr_blocks_INCLUDES="\
-I\${abs_top_srcdir}/gr-blocks/include \
-I\${abs_top_srcdir}/gr-blocks/swig"
        gr_blocks_LA="\${abs_top_builddir}/gr-blocks/lib/libgnuradio-blocks.la"
	gr_blocks_LIBDIRPATH="\${abs_top_builddir}/gr-blocks/lib:\${abs_top_builddir}/gr-blocks/lib/.libs"
	gr_blocks_SWIGDIRPATH="\${abs_top_builddir}/gr-digtial/lib/swig:\${abs_top_builddir}/gr-blocks/swig/.libs:\${abs_top_srcdir}/gr-blocks/swig"
	gr_blocks_PYDIRPATH="\${abs_top_srcdir}/gr-blocks/python"
    fi

    AC_SUBST(gr_blocks_I)
    AC_SUBST(gr_blocks_SWIGDIRPATH)
    AC_SUBST(gr_blocks_PYDIRPATH)

    AC_CONFIG_FILES([\
        gr-blocks/Makefile \
	gr-blocks/gnuradio-blocks.pc \
	gr-blocks/grc/Makefile \
        gr-blocks/include/Makefile \
        gr-blocks/include/gnuradio/Makefile \
        gr-blocks/include/gnuradio/blocks/Makefile \
        gr-blocks/lib/Makefile \
	gr-blocks/python/Makefile \
	gr-blocks/python/run_tests \
	gr-blocks/swig/Makefile \
    ])

    GRC_BUILD_CONDITIONAL(gr-blocks,[
        dnl run_tests is created from run_tests.in.  Make it executable.
        AC_CONFIG_COMMANDS([run_tests_blocks],
			   [chmod +x gr-blocks/python/run_tests])
    ])
])
