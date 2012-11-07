# Copyright 2012 Free Software Foundation, Inc.
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

########################################################################
# Setup the include and linker paths
########################################################################
include_directories(
    ${GR_CTRLPORT_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
    ${GNURADIO_CORE_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    ${CPPUNIT_INCLUDE_DIRS}
)

link_directories(${Boost_LIBRARY_DIRS})

########################################################################
# Run ICE To compile Slice files
########################################################################
EXECUTE_PROCESS(
   COMMAND "${ICE_SLICE2CPP}" "-I${CMAKE_CURRENT_SOURCE_DIR}/../slice"
       "--output-dir=${CMAKE_CURRENT_BINARY_DIR}"
       "${CMAKE_CURRENT_SOURCE_DIR}/../slice/gnuradio.ice"
   )

########################################################################
# Setup library
########################################################################

list(APPEND ctrlport_sources 
    ${CMAKE_CURRENT_SOURCE_DIR}/ice_application_base.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/rpcserver_ice.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/rpcserver_booter_ice.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/rpcserver_booter_aggregator.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/rpcserver_aggregator.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/rpcserver_selector.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/rpcpmtconverters_ice.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/rpcmanager.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/probe_c_impl.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/probe2_c_impl.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/nop_impl.cc
    ${CMAKE_CURRENT_BINARY_DIR}/gnuradio.cpp
)

list(APPEND ctrlport_libs
  ${Boost_LIBRARIES}
  ${ICE_LIBRARIES}
  gruel
  gnuradio-core
)

ADD_LIBRARY(gnuradio-ctrlport SHARED ${ctrlport_sources})
TARGET_LINK_LIBRARIES(gnuradio-ctrlport ${ctrlport_libs})
GR_LIBRARY_FOO(gnuradio-ctrlport RUNTIME_COMPONENT "ctrlport_runtime" DEVEL_COMPONENT "ctrlport_devel")
ADD_DEPENDENCIES(gnuradio-ctrlport gnuradio-core ctrlport_generated_includes ctrlport_generated_swigs)
