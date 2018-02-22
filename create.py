
import argparse
from netCDF4 import Dataset
import datetime 

parser = argparse.ArgumentParser(description='Date:')
parser.add_argument('-d', type=str, help='day of year')
parser.add_argument('-y', type=str, help='year')
parser.add_argument('-v', type=str, help='version')
args = parser.parse_args()

year = args.y
num = args.d
version = args.v

if args.d == None:
	print('No date inputted.')
	print('Please enter date in the format: -d YYYY-MM-DD')

if args.v == None:
	version = 'v01r000'
else:
	version = 'v%sr%s' % (version[:1].zfill(2), version[1:])

#loading in the NC
path = "/disks/icondata/Repository/Archive/LEVEL.0.PRIME/GROUND/EPHEMERIS.PREDICTIVE/"
try:
	iconData = Dataset("%s/%s/ICON_L0P_Ephemeris_Predictive_%s-%s_%s.NC" % (path, year, year, num, version))
except:
	raise Exception('No file matching day and year.')

lat = iconData.variables['LONGITUDE']
lon = iconData.variables['LATITUDE']
alt = iconData.variables['HEIGHT']
doy = iconData.variables['DOY']
hour = iconData.variables['HOUR']
mins = iconData.variables['MINS']
sec = iconData.variables['SEC']
q0 = iconData.variables['Q0_ECI']
q1 = iconData.variables['Q1_ECI']
q2 = iconData.variables['Q2_ECI']
q3 = iconData.variables['Q3_ECI']

coords = []
orient = []
position = (str(lat[0]) + ', ' + str(lon[0])+ ', ' + str(float(alt[0]) * 1000))
q = (str(q0[0]) + ', ' + str(q1[0]) + ', ' + str(q2[0]) + ', ' + str(q3[0]))

#datetime to get date from year and day number
date = datetime.datetime.strptime(str(year) + str(doy[0]),'%Y%j').strftime('%Y-%m-%d')
datetimes = date + 'T' + str(datetime.time(hour[0], mins[0], sec[0])) + '+00:00'
pos_value = ' ["' + datetimes + '", ' +  position
orient_value = ' ["' + datetimes + '", ' +  q
coords.append(pos_value)
orient.append(orient_value)

print('Creating czml')
for i in range(1, len(lat)):
	if str(lat[i]) != '--' and str(lon[i]) != '--' and str(alt[i]) != '--':
		position = (str(lat[i]) + ', ' + str(lon[i])+ ', ' + str(float(alt[i]) * 1000))

	if str(q0[i]) != '--' and str(q1[i]) != '--' and str(q2[i]) != '--' and str(q3[i]) != '--':
		q = (str(q0[i]) + ', ' + str(q1[i]) + ', ' + str(q2[i]) + ', ' + str(q3[i]))

	if str(hour[i]) != '--' and str(mins[i]) != '--' and str(sec[i]) != '--':
		datetimes = date + 'T' + str(datetime.time(hour[i], mins[i], sec[i])) + '+00:00'
		value = ', "' + datetimes + '", ' +  position
		quat = ', "' + datetimes + '", ' +  q
		orient.append(quat)
		coords.append(value)


iconData.close()

formatting = """[{"version": "1.0", "id": "document"}, {"label": {"text": "ICON", "pixelOffset": {"cartesian2": [0.0, 16.0]}, "scale": 0.5, "show": true}, "path": {"show": true, "material": {"solidColor": {"color": {"rgba": [255, 0, 255, 125]}}}, "width": 2, "trailTime": 0, "resolution": 120, "leadTime": 0, "trailTime": 10000},  "billboard": {"image" : "../../SampleData/models/CesiumAir/Cesium-Air.gltf", "scale": 30.0, "sizeInMeters": true, "show": true}, "position": {"interpolationDegree": 5, "referenceFrame": "INTERTIAL", "cartographicDegrees":"""
orient_format = '''], "interpolationAlgorithm": "LAGRANGE"},"orientation":{"interpolationAlgorithm":"LINEAR", "interpolationDegree":1, "unitQuaternion":'''
final_format = ''' ,"id": "ICON"}]'''


#writing to file
name = '%s-%s_%s' % (year, num, version)
f = open('../Documents/Cesium/Apps/ICONData/czml/' + name +'.czml', 'w')
f.write(formatting)
for i in range(len(coords)):
	f.write(coords[i][0:-1])
f.write(orient_format)
for i in range(len(orient)):
	f.write(orient[i][0:-1])
f.write(final_format)
print('Data saved in ' + name + '.czml')
f.close()

