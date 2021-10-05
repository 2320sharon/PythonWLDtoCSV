Contents of the WLD file

```
X-cell size
rotation (usually 0)
rotation (usually 0)
Y-cell size (always negative)
Upper left X
Upper left Y
```

here is the pseudocode for the 4 corners, assuming rotation is zero

- XMin = WorldX - (XCellSize / 2)
- YMax = WorldY - (YCellSize / 2)
- XMax = (WorldX + (Cols \* XCellSize)) - (XCellSize / 2)
- YMin = (WorldY + (Rows \* YCellSize)) - (YCellSize / 2)

coordinate reference system information string, called dataAxisToSRSAxisMapping in the xml file
, that needs to be parsed so the PROJCS info `(["WGS 84 / UTM zone 18N"]) `is extracted
then create a line in a csv per input image that contains the following rows:

1. image filename,
2. Easting min (XMin),
3. Easting max (XMax),
4. Northing min (YMin),
5. Norhting max (YMax),
6. Coordinate Reference System (e.g. wgs 84 / utm zone 18N).

you can use numpy or pandas to create the csv file
For reference, these jpeg/xml/wld files were created from the attached tif using the GDAL command in bash:
` gdal_translate -of JPEG -scale -co worldfile=yes $file "${file%.tif}.jpg"`
