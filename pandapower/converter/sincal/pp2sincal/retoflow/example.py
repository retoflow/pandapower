import os
import shutil

import numpy as np

import pandapower as pp
from pandapower.converter.sincal.pp2sincal.pp2sincal import pp2sincal
from pandapower.converter.sincal.pp2sincal.retoflow.individual_fcts import individual_fcts
from pandapower.converter.sincal.pp2sincal.retoflow.pp_json_2_sqlite import fix_net_for_sql_export
from pandapower.converter.sincal.sincal2pp.sincal2pp import sincal2pp
from pandapower.toolbox import create_continuous_bus_index, create_continuous_elements_index
from pandapower.toolbox.comparison import nets_equal


def convert_pp2sincal(net_pp, sincal_folder_path, sincal_file_name):
    fix_net_for_sql_export(net_pp)
    create_continuous_elements_index(net_pp, 0, add_df_to_reindex={'switch'})
    create_continuous_bus_index(net_pp, 1, True)
    pp.runpp(net_pp)
    pp2sincal(net_pp, sincal_folder_path, file_name, dc_as_sync=True, use_ui=False, sincal_interaction=False,
              individual_fcts=individual_fcts)

    shutil.copy(os.path.join(sincal_folder_path, sincal_file_name.replace('.sin', '') + '_files', 'database.db'),
                os.path.join(sincal_folder_path, sincal_file_name.replace('.sin', '') + '_files', 'database.sqlite'))
    net_new = sincal2pp(os.path.join(sincal_folder_path, sincal_file_name.replace('.sin', '') + '_files', 'database.sqlite'))

    pp.runpp(net_new)

    nets_equal(net_pp, net_new, check_only_results=True, atol=1e-6, exclude_elms=['asymmetric_sgen'])

    assert np.isclose(np.abs(net_pp.asymmetric_sgen.p_a_mw.values).sum(),
                      np.abs(net_new.asymmetric_sgen.p_a_mw.values).sum())
    assert np.isclose(np.abs(net_pp.asymmetric_sgen.p_b_mw.values).sum(),
                      np.abs(net_new.asymmetric_sgen.p_b_mw.values).sum())
    assert np.isclose(np.abs(net_pp.asymmetric_sgen.p_c_mw.values).sum(),
                      np.abs(net_new.asymmetric_sgen.p_c_mw.values).sum())


if __name__ == '__main__':
    net_pp = pp.from_json(r'\path\to\pp\net.json')
    folder_path = r'\path\to\sincal\folder'
    file_name = r'name_of_sincal_net.sin'
    convert_pp2sincal(net_pp, folder_path, file_name)
