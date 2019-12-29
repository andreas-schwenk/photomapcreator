# Photo Map Creator

_Photo Map Creator_ is a small tool written in Python 3 that parses a photo directory and creates an HTML document that renders all photo positions into a map. We use OpenLayers to display maps.

## Example Output

The following screenshot shows an example output.
A corresponding HTML document can be found in maps/fuerteventura2015.html

![alt text](screenshots/fuerteventura2015.png)

## Dependencies

_Photo Map Creator_ makes use of the following Dependencies:

* `gpsphoto`. Install it via `pip3 install gpsphoto`.

* `exiftool`. This dependency is optional and only needed if you have input images that are not in JPEG format (e.g. Apple HEIC). Install it in Linux via `sudo apt-get exiftool`.

## Usage

You can run _Photo Map Creator_ by either CLI or GUI.

### Command Line Interface (CLI)

```
python3 photo-map-creator.py OUTPUT_FILENAME GPS_LATITUDE GPS_LONGITUDE ZOOM PHOTO_DIRECTORY
```

The parameters are given below:

* `OUTPUT_FILENAME`: Name of the output file. The postfix `.html` added by the tool.
* `GPS_LATITUDE`: Decimal Latitude for the initial view. If `0.0` is given, that the latitude from the first photo is taken.
* `GPS_LONGITUDE`: Decimal Latitude for the initial view. If `0.0` is given, that the Longitude from the first photo is taken.
* `ZOOM`: Zoom value for the initial view. E.g. 15
* `PHOTO_DIRECTORY`: Path to your photos.

### Graphical User Interface (GUI)

Start as follows.

```
python3 photo-map-creator.py
```

Parameters are same as with the command line interface.
