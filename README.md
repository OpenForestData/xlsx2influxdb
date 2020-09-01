# XLS2InfluxDB
This application drops data from an XLS to InfluxDB file, heavily based on https://github.com/fabio-miranda/csv-to-influxdb/blob/master/csv-to-influxdb.py.

## Installation

### Requirements
All requirements all stored in requirements.txt file.

To run in container environment you need to install docker and docker-compose.

### Application external dependencies
- InfluxDB ➤ https://www.influxdata.com/

### Application environment variables
- ``DBNAME`` - Database name
- ``INPUT`` - Input file
- ``TIMECOLUMN`` - Timestamp column name. Default: timestamp
- ``SERVER`` - Server address. Default: localhost:8086
- ``TIME_SECCONDS`` - The value defines the time intervals between successive file uploads.

### Application installation (local)

- Run project:
```
$ docker-compose pull
$ docker-compose build
$ docker-compose up
```

## Deployment

## Contribution
The project was performed by Whiteaster sp.z o.o., with register office in Chorzów, Poland - www.whiteaster.com and provided under the GNU GPL v.3 license to the Contracting Entity - Mammal Research Institute Polish Academy of Science in Białowieża, Poland.We are proud to release this project under an Open Source license. If you want to share your comments, impressions or simply contact us, please write to the following e-mail address: info@whiteaster.com