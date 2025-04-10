# -*- coding: utf-8 -*-

# Copyright (c) 2016-2025 by University of Kassel and Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.

from copy import deepcopy

import pandas as pd
import pytest

from pandapower.networks.power_system_test_cases import case9
from pandapower.plotting.plotting_toolbox import set_line_geodata_from_bus_geodata
from pandapower.plotting.simple_plot import simple_plot


def test_set_line_geodata_from_bus_geodata():
    net = case9()
    bus_geo_data = deepcopy(net.bus.geo)

    empty_line_geo = pd.Series('null', index=net.line.index, dtype=object)  # ensure that line geo data
    assert not net.bus.geo.loc[net.bus.geo == 'null'].any()  # ensure that bus geo data is available

    simple_plot(net, show_plot=False)  # test that plotting works with case9 file

    # --- create line geo data from complete net.bus.geo to empty net.line.geo
    net.line.geo = deepcopy(empty_line_geo)  # ensure that line geo data is missing
    set_line_geodata_from_bus_geodata(net)
    assert not net.line.geo.loc[net.line.geo == 'null'].any()
    simple_plot(net, show_plot=False)  # test that plotting works with case9 file

    # --- ensure that set_line_geodata_from_bus_geodata() can also handle cases where all geodata
    # are available already
    set_line_geodata_from_bus_geodata(net)

    # --- create line geo data from complete net.bus.geo to incomplete net.line.geo
    net.line.at[2, "geo"] = 'null'
    net.line.at[4, "geo"] = 'null'
    set_line_geodata_from_bus_geodata(net)
    assert not net.line.geo.loc[net.line.geo == 'null'].any()
    simple_plot(net, show_plot=False)  # test that plotting works with case9 file

    # --- create line geo data from complete net.bus.geo to incomplete net.line.geo using overwrite
    net.line.at[2, "geo"] = 'null'
    net.line.at[4, "geo"] = 'null'
    set_line_geodata_from_bus_geodata(net, overwrite=True)
    assert not net.line.geo.loc[net.line.geo == 'null'].any()
    simple_plot(net, show_plot=False)  # test that plotting works with case9 file

    # --- create line geo data from incomplete net.bus.geo to incomplete net.line.geo
    # (-> no warning expected since all missing data can be filled by available bus data)
    net.bus.at[2, "geo"] = 'null'
    net.bus.at[4, "geo"] = 'null'
    net.line.at[0, "geo"] = 'null'
    net.line.at[5, "geo"] = 'null'
    set_line_geodata_from_bus_geodata(net)
    assert not net.line.geo.loc[net.line.geo == 'null'].any()
    net.bus.at[2, "geo"] = bus_geo_data.at[2]
    net.bus.at[4, "geo"] = bus_geo_data.at[4]
    simple_plot(net, show_plot=False)  # test that plotting works with case9 file

    # --- create line geo data from incomplete net.bus.geo to incomplete net.line.geo
    # using line_index (-> no warning expected since all missing data can be filled by available bus
    # data)
    net.bus.at[2, "geo"] = 'null'
    net.bus.at[4, "geo"] = 'null'
    net.line.at[6, "geo"] = 'null'
    net.line.at[7, "geo"] = 'null'
    set_line_geodata_from_bus_geodata(net, line_index=[6, 7])
    assert not net.line.geo.loc[net.line.geo == 'null'].any()
    net.bus.at[2, "geo"] = bus_geo_data.at[2]
    net.bus.at[4, "geo"] = bus_geo_data.at[4]
    simple_plot(net, show_plot=False)  # test that plotting works with case9 file

    # --- create line geo data from incomplete net.bus.geo to empty net.line.geo
    # (-> warning expected)
    net.bus.at[2, "geo"] = 'null'
    net.bus.at[4, "geo"] = 'null'
    net.line.geo = deepcopy(empty_line_geo)  # ensure that line geo data is missing
    set_line_geodata_from_bus_geodata(net)


if __name__ == "__main__":
    pytest.main([__file__])
