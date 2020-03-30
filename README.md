# Xslx 2 influxdb

W zasadzie szkic skryptu wrzucającego dane. Do poprawy.

### Wykorzystanie

Aby uruchomić influxdb oraz grafanę:  
```
$ docker-compose pull
$ docker-compose up
```

Użytkownik na grafanę:  
test/test

Przykład wykorzystaina skryptu:
```
$ python csv-to-influxdb.py --input dane_meteo_2011_05_Bialowieza.xlsx --dbname csv --create --timecolumn data/godzina -tf "%Y-%m-%d %H:%M:%S" -d ";"
```