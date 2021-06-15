import tempfile
import subprocess

import xarray as xr


def run_fs_cmd(fout_path, cmd, fin_path):
    if isinstance(fin_path, list):
        fin_path = " ".join(map(str, fin_path))
    subprocess.run(f"{cmd} {fin_path} {fout_path}", shell=True)


def data_to_data(func, newvar=None):
    def _func(data, *args):
        with tempfile.NamedTemporaryFile("r") as fout, \
             tempfile.NamedTemporaryFile("r") as fin:
            data.to_netcdf(fin.name)
            func(fout.name, fin.name, *args)
            res = xr.load_dataset(fout.name, engine="netcdf4")
        if not isinstance(data, xr.DataArray):
            return res
        newvar_name = newvar if newvar is not None else data.name
        return res[newvar_name]
    return _func