#!/bin/bash

for ARGUMENT in "$@"
do

    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   

    case "$KEY" in
            DBNAME)              DBNAME=${VALUE} ;;
            INPUT)    INPUT=${VALUE} ;;     
            TIMECOLUMN)    INPUT=${VALUE} ;;
            SERVER)    INPUT=${VALUE} ;;
            TIME_SECCONDS)    INPUT=${VALUE} ;;
            *)   
    esac    


done

echo "=== Parametry ==="
echo "DBNAME = $DBNAME"
echo "INPUT = $INPUT" 
echo "TIMECOLUMN = $TIMECOLUMN" 
echo "SERVER = $SERVER"
echo "TIME_SECCONDS = $TIME_SECCONDS"
echo "================="


while true
do
    python /app/main.py --server $SERVER --dbname $DBNAME --input $INPUT --timecolumn $TIMECOLUMN -d ";" --field_columns "wilg,temp >2m,ciś,opad,nasłon,temp < 2m,pokrywa śnieżna,temp <2m min,temp <2m max,Vwmax,Vwsr,Vwmin,kierunek wsr,kierunek wmax,kierunek wmin" --timeformat "%Y-%m-%d %H:%M:%S"
    sleep $TIME_SECCONDS
done
