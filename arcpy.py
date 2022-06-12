# Import the system modules
from pathlib import Path
import arcpy
from arcpy.sa import Hillshade

processing_env = Path("E:\Angola\arcpy_env")

# Set the analysis environments
arcpy.env.workspace = r"E:\Angola\arcpy_env"


# Set the local variables
in_dem = Path("E:\Angola\ALOS_DEM\AP_01645_FBS_F6920_RT1\AP_01645_FBS_F6920_RT1.dem.tif")

# Execute the Hillshade function
def hillshade_loop(in_dem):
    for i in [180,225,270,315]:
        out_hillshade = "hillshade_" + str(i) + ".tif"  # Set the output raster name    
        out_hillshade_raster = Hillshade(in_dem, i, 45, 1)
        out_hillshade_raster.save(Path(processing_env,out_hillshade))

# Save the output
