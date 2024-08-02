import pandas as pd


def fix_net_for_sql_export(net):
    station_buses = net.bus[~net.bus.substation.isnull()]
    for station_idx, buses in station_buses.groupby("substation"):
        station_geo = net.substation.geo.at[station_idx]
        net.bus.loc[buses.index.tolist(), "geo"] = [station_geo] * len(buses)

    data_bus = {
        "x": [],
        "y": [],
    }
    buses_with_geo = net.bus[~net.bus.geo.isnull()]
    for bus in buses_with_geo.itertuples():
        coords = bus.geo["coordinates"]
        data_bus["x"].append(coords[1])
        data_bus["y"].append(coords[0])
    net["bus_geodata"] = pd.DataFrame(data_bus, index=buses_with_geo.index)

    data_line = {
        "coords": [],
    }
    lines_with_geo = net.line[~net.line.geo.isnull()]
    for line in lines_with_geo.itertuples():
        coords = line.geo["coordinates"]
        data_line["coords"].append([[c[1], c[0]] for c in coords])
    net["line_geodata"] = pd.DataFrame(data_line, index=lines_with_geo.index)

    del net["std_types"]["converter"]
    del net["area"]
    for key in net.keys():
        if not isinstance(net[key], pd.DataFrame):
            continue
        for col in ["geo", "substation_geo"]:
            if col in net[key].columns:
                del net[key][col]


if __name__ == "__main__":
    import pandapower as pp

    net = pp.from_json(r"/path/to/net.json")
    fix_net_for_sql_export(net)
    pp.to_json(net, r"/save/to/path/net.json")

