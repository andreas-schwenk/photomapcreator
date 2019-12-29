# Photo Map Creator

_Photo Map Creator_ is a small tool written in [Python 3](https://www.python.org/download/releases/3.0/).
It parses a photo directory and creates an HTML document that shows all GPS positions within an embedded map.
We use [OpenLayers](https://openlayers.org) to render maps.

## Example Output

The following screenshot shows an example output.
A corresponding HTML document can be found in this repository [here](maps/fuerteventura2015.html).

![alt text](screenshots/fuerteventura2015.png)

## Dependencies

[Python 3](https://www.python.org/download/releases/3.0/) must be installed in order to run _Photo Map Creator_.
Furthermore you need at least the first of the following dependencies:

* `gpsphoto`: Install it via `pip3 install gpsphoto`.
* `exiftool`: This dependency is optional. It is only needed, if you like to process non-JPEG input images (e.g. Apple HEIC). Install it in Linux via `sudo apt-get exiftool`.

## Usage

You can run _Photo Map Creator_ by either CLI or GUI. The output is always written into the `maps/` directory.

### Command Line Interface (CLI)

```
python3 photo-map-creator.py OUTPUT_FILENAME GPS_LATITUDE GPS_LONGITUDE ZOOM PHOTO_DIRECTORY
```

The parameters are given below:

* `OUTPUT_FILENAME`: Name of the output file. The postfix `.html` added by the tool.
* `GPS_LATITUDE`: Signed decimal Latitude for the initial view. If `0.0` is given, that the latitude from the first photo is taken.
* `GPS_LONGITUDE`: Signed decimal Latitude for the initial view. If `0.0` is given, that the Longitude from the first photo is taken.
* `ZOOM`: Zoom value for the initial view. E.g. 15
* `PHOTO_DIRECTORY`: Path to your photos.

Example:

```
python3 photo-map-creator.py amsterdam 52.3667 4.8945 15 /Users/andi/Pictures/2019/Amsterdam
```

### Graphical User Interface (GUI)

Start as follows.

```
python3 photo-map-creator.py
```

Parameters are same as with the command line interface.
