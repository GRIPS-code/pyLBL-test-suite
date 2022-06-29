from argparse import ArgumentParser
from netCDF4 import Dataset as ncDataset
from numpy import histogram, abs, max, mean, min, nonzero
from pyLBL import Database, Spectroscopy
from xarray import Dataset


def main(input_path, database_path, output_path):
    # Read input data.
    with ncDataset(input_path, "r") as dataset:
        grid = dataset["wavenumber"][:]
        tau = dataset["optical_depth"][:]
        pressure = [dataset["pressure"][...],]
        temperature = [dataset["temperature"][...],]
        xh2o = [dataset["water_vapor"][...],]

    def variable(data, units, standard_name):
        return (["z",], data, {"units": units, "standard_name": standard_name})

    # Create atmospheric dataset.
    atmosphere = Dataset(
        data_vars={
            "play": variable(pressure, "Pa", "air_pressure"),
            "tlay": variable(temperature, "K", "air_temperature"),
            "xh2o": variable(xh2o, "mol mol-1", "mole_fraction_of_water_vapor_in_air"),
        },
    )

    # Calcluate spectra.
    database = Database(database_path)
    spectra = Spectroscopy(atmosphere, grid, database).compute_absorption(remove_pedestal=False)
    spectra.to_netcdf(output_path)

    # Calculate differences.
    abs_pylbl = spectra.data_vars["H2O_absorption"].values[0, 0, :]
    error = 100. * abs(tau[:] - abs_pylbl[:]) / tau[:]
    print("Differences:")
    print("---------------------------------------")
    print("Maximum:                            {:10.8e} %".format(max(error)))
    print("Minimum:                            {:10.8e} %".format(min(error)))
    print("Mean:                               {:10.8e} %".format(mean(error)))
    print("Standard deviation:                 {:10.8e}".format(mean(error)))
    for x in [10, 5, 2, 1]:
        n = 100.*(nonzero(error > x)[0].size/grid.size)
        print("% of points with > {:02d}% difference:  {}".format(x, n))


if __name__ == "__main__":
    parser = ArgumentParser("Test water vapor lines (no continuum) against RFM.")
    parser.add_argument("input_path", help="Path to input file.")
    parser.add_argument("database_path", help="HITRAN API key.")
    args = parser.parse_args()
    main(args.input_path, args.database_path, f"pylbl-{args.input_path}")
