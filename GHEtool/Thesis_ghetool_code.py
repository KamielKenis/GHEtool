"""
This code determines the required depth of the borehole for a given load profile that is imported in the file.
"""
import pygfunction as gt
import pandas as pd
import numpy as np

from GHEtool import *

# initiate ground data
data = GroundTemperatureGradient(1.75, 10, 2500000, 3)
fluid_data = FluidData(0.45, 0.425, 1045, 3720, 1e-3)
pipe_data = SingleUTube(0.73, 0.0164, 0.0167, 0.39, 0.0375, 0.000001)
borefield_gt = gt.boreholes.rectangle_field(1, 1, 1, 1, 182, 1, 0.075)


# initiate borefield
borefield = Borefield()

# set borefield
borefield.set_borefield(borefield_gt)

# set ground data in borefield
borefield.set_ground_parameters(data)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)

# set temperature boundaries
borefield.set_max_avg_fluid_temperature(35)  # maximum temperature
borefield.set_min_avg_fluid_temperature(0)  # minimum temperature



file_path = "Qbor_pos_1_2_10_average_k1.75_VHC2500_182m.csv"
df = pd.read_csv(file_path, sep=",")

# Select only the last column
Q_avg = df.iloc[:, -1].values
Q_avg_kW = Q_avg/1000

positive_values = np.where(Q_avg_kW > 0, Q_avg_kW, 0)
negative_values = np.where(Q_avg_kW < 0, -Q_avg_kW, 0)

load = HourlyGeothermalLoad()
load.set_hourly_heating(positive_values)
# load.set_hourly_cooling(negative_values)
borefield.load = load

borefield.load.simulation_period = 20


# size the borefield and plot the resulting temperature evolution
depth = borefield.size(182, use_constant_Rb=False, L4_sizing=True)
print(borefield.Rb)
print(depth)
borefield.print_temperature_profile()

