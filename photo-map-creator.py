# ******************************************************************************
# *                                                                            *
# *                   P H O T O   M A P   C R E A T O R                        *
# *                                                                            *
# *  Copyright 2019 Andreas Schwenk                                            *
# *  www.arts-and-sciences.com                                                 *
# *                                                                            *
# *  This program is free software: you can redistribute it and/or modify      *
# *  it under the terms of the GNU General Public License as published by      *
# *  the Free Software Foundation, either version 3 of the License, or         *
# *  (at your option) any later version.                                       *
# *                                                                            *
# *  This program is distributed in the hope that it will be useful,           *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             *
# *  GNU General Public License for more details.                              *
# *                                                                            *
# *  You should have received a copy of the GNU General Public License         *
# *  along with this program.  If not, see <https://www.gnu.org/licenses/>.    *
# *                                                                            *
# ******************************************************************************

LANG = 1   # setlanguage: { 0 := English, 1 := German }

import sys

if sys.version_info[0] < 3:
	raise Exception("REQUIRES PYTHON IN VERSION 3!")

import os
import glob
import subprocess
import time
from GPSPhoto import gpsphoto      # pip3 install gpsphoto piexif
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import distutils.spawn

# exiftool is optional and only needed for non-JPEG pictures (e.g. Apple HEIF)
# (install it in linux via  $sudo apt-get exiftool)
EXIFTOOL_INSTALLED = distutils.spawn.find_executable("exiftool") != None

def process(location_name, view_zoom, view_lat, view_lon, photo_directory):

	print('===== parameters =====')
	print('name=' + location_name)
	print('zoom=' + str(view_zoom))
	print('lat=' + str(view_lat))
	print('lon=' + str(view_lon))
	print('dir=' + photo_directory)

	HTML_template = '''
	<html>
		<head>
			<title>*TITLE*</title>
			<script src="http://www.openlayers.org/api/OpenLayers.js"></script>
		</head>
		<body>
			<div id="mapdiv"></div>
			<script>
				map = new OpenLayers.Map("mapdiv");
				map.addLayer(new OpenLayers.Layer.OSM());

				var markers = new OpenLayers.Layer.Markers("Markers");
				map.addLayer(markers);

				function add(lat, lon) {
					var size = new OpenLayers.Size(16,16);
					var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
					var icon = new OpenLayers.Icon('../img/marker.png',size,offset);
					var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject() );
					var marker = new OpenLayers.Marker(lonLat, icon);
					markers.addMarker(marker);
				}
				*MARKERS*
				var centerLonLat = new OpenLayers.LonLat(*VIEW_GPS*).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject() );
				var zoom = *VIEW_ZOOM*;
				map.setCenter (centerLonLat, zoom);
			</script>
		</body>
	</html>
	'''

	marker_str = '\n'

	if photo_directory.endswith('/'):
		photo_directory += '*'
	else:
		photo_directory += '/*'

	for file in glob.glob(photo_directory):
		if file.startswith("."):
			continue
		if os.path.isdir(file):
			continue

		if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".jpeg") or file.endswith(".JPEG"):
			# --- (OPTION A) THE FOLLOWING CODE NEEDS PYTHON3 LIBRARY 'GPSPHOTO' (does NOT work with photos in HEIC format!) --
			try:
				gpsdata = gpsphoto.getGPSData(file)
				if "Latitude" in gpsdata:
					lat = gpsdata["Latitude"]
					lon = gpsdata["Longitude"]
					print(file + ':' + str(lat) + ',' + str(lon))
					marker_str += '\t\t\tadd(' + str(lat) + ',' + str(lon) + ');\n'
			except:
				print('warning: failed to process image ' + file)

		elif EXIFTOOL_INSTALLED:
			# --- (OPTION B) THE FOLLOWING CODE NEEDS 'EXIFTOOL' TO BE INSTALLED (much slower than option A, but works with (nearly) all image and video formats) --
			gps = subprocess.check_output("exiftool -c '%+.6f' -GPSPosition -s -s -s " + file, shell=True).decode("utf-8")
			if ',' in gps:
				[lat, lon] = gps.split(",")
				lat = float(lat)
				lon = float(lon)
				print(file + ':' + str(lat) + ',' + str(lon))
				marker_str += '\t\t\tadd(' + str(lat) + ',' + str(lon) + ');\n'
				if view_lat==0.0 and view_lon==0.0:
					view_lat = lat
					view_lon = lon

	file_content = HTML_template.replace('*TITLE*',location_name).replace('*MARKERS*', marker_str).replace('*VIEW_GPS*',str(view_lon) + ',' + str(view_lat)).replace('*VIEW_ZOOM*',str(view_zoom))

	file = open("maps/" + location_name + ".html", "w")
	file.write(file_content)
	file.close()


if __name__ == '__main__':

	location_name = ''
	view_zoom = 14
	view_lat = 0.0
	view_lon = 0.0
	photo_directory = ''

	STR_TITLE = ['Photo Map Creator - 2019 by Andreas Schwenk', 'Photo Map Creator - 2019 by Andreas Schwenk']
	STR_NAME = ['Output Filename', 'Name der Ausgabedatei']
	STR_LAT = ['GPS Lat (optional)', 'GPS Lat (optional)']
	STR_LON = ['GPS Lon (optional)', 'GPS Lon (optional)']
	STR_ZOOM = ['Zoom (optional)', 'Zoom (optional)']
	STR_PHOTO_PATH = ['Photo Path', 'Fotoverzeichnis']
	STR_WAIT = ['PLEASE WAIT', 'BITTE WARTEN']
	STR_SET_PHOTO_PATH = ['Set Photo Path', 'Fotoverzeichnis setzen']
	STR_BUILD = ['Build', 'Erzeugen']
	STR_READY = ['Ready', 'Fertig']
	STR_ERR_NAME_EMPTY = ['ERROR: NAME IS NOT SET', 'FEHLER: NAME NICHT GESETZT']
	STR_ERR_DIR_NOT_SET = ['ERROR: DIRECTORY IS NOT SET', 'FEHLER: FOTOVERZEICHNIS NICHT GESETZT']

	if len(sys.argv) == 1:

		master = tk.Tk()
		master.title(STR_TITLE[LANG])
		master.geometry("520x320")

		tk.Label(master, text=STR_NAME[LANG]).grid(row=0,sticky='W')
		tk.Label(master, text=STR_LAT[LANG]).grid(row=1,sticky='W')
		tk.Label(master, text=STR_LON[LANG]).grid(row=2,sticky='W')
		tk.Label(master, text=STR_ZOOM[LANG]).grid(row=3,sticky='W')
		tk.Label(master, text=STR_PHOTO_PATH[LANG]).grid(row=4,sticky='W')
		lpath = tk.StringVar()
		tk.Label(master, textvariable=lpath).grid(row=4,column=1,sticky='W')
		linfo = tk.StringVar()
		tk.Label(master, textvariable=linfo, fg='red', font=("Arial", 16)).grid(row=6,column=1,sticky='W')

		entryLocationName = tk.Entry(master)
		entryViewLat = tk.Entry(master)
		entryViewLat.insert(tk.END, str(view_lat))
		entryViewLon = tk.Entry(master)
		entryViewLon.insert(tk.END, str(view_lon))
		entryViewZoom = tk.Entry(master)
		entryViewZoom.insert(tk.END, str(view_zoom))

		entryLocationName.grid(row=0, column=1)
		entryViewLat.grid(row=1, column=1)
		entryViewLon.grid(row=2, column=1)
		entryViewZoom.grid(row=3, column=1)

		def setPhotoPath():
			global photo_directory
			photo_directory = filedialog.askdirectory()
			lpath.set(photo_directory)
			#print(photo_directory)

		def build():
			global location_name, view_zoom, view_lat, view_long
			linfo.set(STR_WAIT[LANG])
			master.update()
			time.sleep(1)
			location_name = entryLocationName.get()
			view_lat = float(entryViewLat.get().replace(',','.'))
			view_lon = float(entryViewLon.get().replace(',','.'))
			view_zoom = int(entryViewZoom.get())
			if len(location_name)==0:
				linfo.set(STR_ERR_NAME_EMPTY[LANG])
				return
			if len(photo_directory)==0:
				linfo.set(STR_ERR_DIR_NOT_SET[LANG])
				return
			process(location_name, view_zoom, view_lat, view_lon, photo_directory)
			linfo.set(STR_READY[LANG])

		tk.Button(master, text=STR_SET_PHOTO_PATH[LANG], command=setPhotoPath, highlightbackground='#000000').grid(row=6, column=0, sticky=tk.W, pady=4)
		tk.Button(master, text=STR_BUILD[LANG], command=build, highlightbackground='#000000').grid(row=7, column=0, sticky=tk.W, pady=4)

		master.update()
		master.mainloop()

	elif len(sys.argv) == 6:
		location_name = sys.argv[1]
		view_zoom = sys.argv[4] # 15
		view_lat = sys.argv[2] # 52.3667
		view_lon = sys.argv[3] # 4.8945
		photo_directory = sys.argv[5]
		process(location_name, view_zoom, view_lat, view_lon, photo_directory)

	else:
		print('usage: /usr/local/bin/python3 create-photo-map.py LOCATION_NAME GPS_LATITUDE GPS_LONGITUDE ZOOM PHOTO_DIRECTORY')
		sys.exit(-1)
