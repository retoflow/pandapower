import copy
import os
import sqlite3

import numpy as np
import pandas as pd


def individual_fcts(net, file_name, output_folder):
    con = _add_additional_tables(file_name, output_folder)
    _pandapower_objects(net, con)


def _pandapower_objects(net, con):
    _nodes(net, con)
    _loads(net, con)
    _sgens(net, con)
    _asgens(net, con)
    _gen(net, con)
    _storage(net, con)
    _trafo(net, con)
    _line(net, con)
    _switch(net, con)


def _nodes(net, con):
    nodes = net['sincal_lookup']['table_name'] == 'node'
    data = copy.deepcopy(net['bus'].loc[net['sincal_lookup'].loc[nodes, 'pp_index'].values, :])
    data_geo = copy.deepcopy(net['bus_geodata'].loc[net['sincal_lookup'].loc[nodes, 'pp_index'].values, :])
    data['znf_id'] = None
    data['status'] = None
    # ToDo: After Update remove!
    data['isu_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, nodes, con)


def _loads(net, con):
    loads = net['sincal_lookup']['pp_element'] == 'load'
    data = copy.deepcopy(net['load'].loc[net['sincal_lookup'].loc[loads, 'pp_index'].values, :])
    buses = data.bus.values
    data_geo = copy.deepcopy(net['bus_geodata'].loc[buses, :])
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, loads, con)


def _sgens(net, con):
    sgens = net['sincal_lookup']['pp_element'] == 'sgen'
    data = copy.deepcopy(net['sgen'].loc[net['sincal_lookup'].loc[sgens, 'pp_index'].values, :])
    buses = data.bus.values
    data_geo = copy.deepcopy(net['bus_geodata'].loc[buses, :])
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, sgens, con)


def _asgens(net, con):
    asgens = net['sincal_lookup']['pp_element'] == 'asymmetric_sgen'
    data = copy.deepcopy(net['asymmetric_sgen'].loc[net['sincal_lookup'].loc[asgens, 'pp_index'].values, :])
    buses = data.bus.values
    data_geo = copy.deepcopy(net['bus_geodata'].loc[buses, :])
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, asgens, con)


def _ext_grid(net, con):
    ext_grids = net['sincal_lookup']['pp_element'] == 'ext_grid'
    data = copy.deepcopy(net['ext_grid'].loc[net['sincal_lookup'].loc[ext_grids, 'pp_index'].values, :])
    buses = data.bus.values
    data_geo = copy.deepcopy(net['bus_geodata'].loc[buses, :])
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['gis_id'] = None
    data['sap_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, ext_grids, con)


def _gen(net, con):
    gens = net['sincal_lookup']['pp_element'] == 'gen'
    data = copy.deepcopy(net['gen'].loc[net['sincal_lookup'].loc[gens, 'pp_index'].values, :])
    buses = data.bus.values
    data_geo = copy.deepcopy(net['bus_geodata'].loc[buses, :])
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['gis_id'] = None
    data['sap_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, gens, con)


def _storage(net, con):
    storages = net['sincal_lookup']['pp_element'] == 'storage'
    data = copy.deepcopy(net['storage'].loc[net['sincal_lookup'].loc[storages, 'pp_index'].values, :])
    buses = data.bus.values
    data_geo = copy.deepcopy(net['bus_geodata'].loc[buses, :])
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['gis_id'] = None
    data['sap_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, storages, con)


def _dc_line(net, con):
    dc_lines = net['sincal_lookup']['pp_element'] == 'dc_line'
    data = copy.deepcopy(net['dc_line'].loc[net['sincal_lookup'].loc[dc_lines, 'pp_index'].values, :])
    data_geo = copy.deepcopy(pd.DataFrame([[None, None]] * len(data), columns=['x', 'y']))
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['gis_id'] = None
    data['sap_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, dc_lines, con)


def _trafo(net, con):
    trafos = net['sincal_lookup']['pp_element'] == 'trafo'
    data = copy.deepcopy(net['trafo'].loc[net['sincal_lookup'].loc[trafos, 'pp_index'].values, :])
    data_geo = copy.deepcopy(pd.DataFrame([[None, None]] * len(data), columns=['x', 'y']))
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, trafos, con)


def _line(net, con):
    lines = net['sincal_lookup']['pp_element'] == 'line'
    data = copy.deepcopy(net['line'].loc[net['sincal_lookup'].loc[lines, 'pp_index'].values, :])
    data_geo = copy.deepcopy(pd.DataFrame([[None, None]] * len(data), columns=['x', 'y']))
    data['sap_id'] = data['SAP_Equi'].values
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, lines, con)


def _switch(net, con):
    switches = net['sincal_lookup']['pp_element'] == 'switch'
    data = copy.deepcopy(net['switch'].loc[net['sincal_lookup'].loc[switches, 'pp_index'].values, :])
    data_geo = copy.deepcopy(pd.DataFrame([[None, None]] * len(data), columns=['x', 'y']))
    data['znf_id'] = None
    # ToDo: After Update remove!
    data['status'] = None
    data['isu_id'] = None
    data['gis_id'] = None
    data['sap_id'] = None
    data['Bezeichnung'] = None

    _insert_data(net, data, data_geo, switches, con)


def _insert_data(net, data, data_geo, mask, con):
    insert_query = (
            'INSERT INTO %s ("table_name", id, pandapower_element, pandapower_element_index, name, sincal_name, '
            'GIS_id, SAP_id, ISU_ID, ZNF_ID, COORD_x, COORD_y, status, Bezeichnung) VALUES '
            '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' % 'PandapowerObjects')

    ar = np.concatenate([[net['sincal_lookup'].loc[mask, 'table_name'].values,
                          net['sincal_lookup'].loc[mask, 'id'].values,
                          net['sincal_lookup'].loc[mask, 'pp_element'].values, data.index.values, data.name.values,
                          data.Sinc_Name.values, data.gis_id.values, data.sap_id.values, data.isu_id.values,
                          data.znf_id.values, data_geo.x.values, data_geo.y.values, data.status.values,
                          data.Bezeichnung.values]], axis=1).T.tolist()
    cur = con.cursor()
    cur.executemany(insert_query, ar)
    con.commit()


def _add_additional_tables(file_name, output_folder):
    con = sqlite3.connect(os.path.join(output_folder, file_name.replace('.sin', '') + '_files', 'database.db'))
    cur = con.cursor()
    for table in ['PandapowerObjects', 'PandapowerNetworks', 'PandapowerConfiguration', 'PandapowerResults']:
        cur.execute(f"DROP TABLE IF EXISTS {table}")
    con.commit()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS PandapowerObjects (
        table_name TEXT,
        id INTEGER,
        pandapower_element TEXT, 
        pandapower_element_index INTEGER, 
        name TEXT,
        sincal_name TEXT,
        GIS_id INTEGER, 
        SAP_id TEXT,
        ISU_ID INTEGER, 
        ZNF_ID TEXT, 
        COORD_x REAL, 
        COORD_y REAL,
        status TEXT,
        Bezeichnung TEXT
    );
    '''
    cur.execute(create_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS PandapowerNetworks (
        IpSum TEXT 
    );
    '''
    cur.execute(create_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS PandapowerConfiguration (
        IpSum TEXT 
    );
    '''
    cur.execute(create_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS PandapowerResults (
        IpSum TEXT 
    );
    '''
    cur.execute(create_table_query)

    con.commit()
    return con
