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
# Setup dependencies
########################################################################
include(GrBoost)

FIND_PACKAGE(ICE)

########################################################################
# Register component
########################################################################
include(GrComponent)

GR_REGISTER_COMPONENT("gr-ctrlport" ENABLE_GR_CTRLPORT
    ENABLE_GRUEL
    Boost_FOUND
    ICE_FOUND
    ENABLE_GR_CORE
)

GR_SET_GLOBAL(GR_CTRLPORT_INCLUDE_DIRS
    ${CMAKE_CURRENT_SOURCE_DIR}/lib
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_BINARY_DIR}/lib
    ${CMAKE_CURRENT_BINARY_DIR}/include
    ${ICE_INCLUDE_DIR}
)

SET(GR_PKG_CTRL_EXAMPLES_DIR ${GR_PKG_DATA_DIR}/examples/ctrlport)

########################################################################
# Begin conditional configuration
########################################################################
if(ENABLE_GR_CTRLPORT)


########################################################################
# Setup CPack components
########################################################################
include(GrPackage)
CPACK_SET(CPACK_COMPONENT_GROUP_CONTROLPORT_DESCRIPTION "GNU Radio ControlPort Blocks")

CPACK_COMPONENT("ctrlport_runtime"
    GROUP        "ControlPort"
    DISPLAY_NAME "Runtime"
    DESCRIPTION  "Runtime"
    DEPENDS      "core_runtime"
)

CPACK_COMPONENT("ctrlport_devel"
    GROUP        "ControlPort"
    DISPLAY_NAME "Development"
    DESCRIPTION  "C++ headers, package config, import libraries"
    DEPENDS      "core_devel"
)

CPACK_COMPONENT("ctrlport_python"
    GROUP        "ControlPort"
    DISPLAY_NAME "Python"
    DESCRIPTION  "Python modules for runtime; GRC xml files"
    DEPENDS      "core_python;ctrlport_runtime"
)

CPACK_COMPONENT("ctrlport_swig"
    GROUP        "ControlPort"
    DISPLAY_NAME "SWIG"
    DESCRIPTION  "SWIG development .i files"
    DEPENDS      "core_swig;ctrlport_python;ctrlport_devel"
)

########################################################################
# Create Pkg Config File
########################################################################
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/gnuradio-ctrlport.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-ctrlport.pc
@ONLY)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-ctrlport.pc
    DESTINATION ${GR_LIBRARY_DIR}/pkgconfig
    COMPONENT "ctrlport_devel"
)


########################################################################
# Setup preferences file and installation information
########################################################################
SET(GR_PKG_CTRL_SLICE_DIR ${GR_PKG_DATA_DIR}/ctrlport)
file(TO_NATIVE_PATH ${CMAKE_INSTALL_PREFIX}/${GR_PKG_CTRL_SLICE_DIR} slicedir)

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/ctrlport.conf.in
    ${CMAKE_CURRENT_BINARY_DIR}/ctrlport.conf
@ONLY)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/ctrlport.conf
    DESTINATION ${GR_PREFSDIR}
    COMPONENT "grc"
)

########################################################################
# Add subdirectories
########################################################################
add_subdirectory(include/ctrlport)
add_subdirectory(lib)
add_subdirectory(slice)
if(ENABLE_PYTHON)
    add_subdirectory(swig)
    add_subdirectory(python)
    add_subdirectory(grc)
endif(ENABLE_PYTHON)
add_subdirectory(examples)
add_subdirectory(doc)


endif(ENABLE_GR_CTRLPORT)

