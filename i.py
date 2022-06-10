from pci.line import line
from pci.fexport import fexport

tif_file = r"E:\arcpro\hillshadex.tif"
pix_file = r"E:\arcpro\hillshadex.pix"
shp_file = r"E:\arcpro\hillshadex.shp"

line(fili=tif_file, filo=pix_file, dbic=[1])
fexport(fili=pix_file, filo=shp_file, dbvs=[1], ftype="shp")
