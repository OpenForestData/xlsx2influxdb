# Xslx 2 influxdb

W zasadzie szkic skryptu wrzucającego dane. Do poprawy.  

Python 3.8

### Wykorzystanie

Aby uruchomić całość:  
```
$ docker-compose pull
$ docker-compose build
$ docker-compose up
```

Użytkownik na grafanę (http://localhost:3000/):  
test/test

Instalacja requirements.txt:  
```
pip install -r requirements.txt
```

Przykłady wykorzystaina skryptu (bez dockera):
```
$ python csv-to-influxdb.py --input dane_meteo_2011_05_Bialowieza.xlsx --dbname csv --create --timecolumn data/godzina -tf "%Y-%m-%d %H:%M:%S" -d ";"
```

```
$ python csv-to-influxdb.py --input dane_meteo_2011_05_Bialowieza.xlsx --dbname csv --create --timecolumn data/godzina -tf "%Y-%m-%d %H:%M:%S" -d ";" --fieldcolumns "wilg,temp >2m,ciś,opad,nasłon,temp < 2m,pokrywa śnieżna,temp <2m min,temp <2m max,Vwmax,Vwsr,Vwmin,kierunek wsr,kierunek wmax,kierunek wmin"
```
