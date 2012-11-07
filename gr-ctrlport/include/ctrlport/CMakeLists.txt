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

INSTALL(FILES
    api.h
    ice_application_base.h
    ice_server_template.h
    rpccallbackregister_base.h
    rpcmanager_base.h
    rpcmanager.h
    rpcpmtconverters_ice.h
    rpcregisterhelpers.h
    rpcserver_aggregator.h
    rpcserver_base.h
    rpcserver_booter_aggregator.h
    rpcserver_booter_base.h
    rpcserver_booter_ice.h
    rpcserver_selector.h
    probe_c.h
    probe2_c.h
    nop.h
    DESTINATION ${GR_INCLUDE_DIR}/gnuradio/ctrlport
    COMPONENT "ctrlport_devel"
)

