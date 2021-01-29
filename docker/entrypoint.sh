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
    python /app/main.py --server $SERVER --dbname $DBNAME -u meteo -p STP1quARSPec --input $INPUT --timecolumn $TIMECOLUMN -d "t" --field_columns "U200,T200,Vwmin,Vwmax,Vwsred,Kwmin,Kwmax,Kwsred,T5,T5max,T5min,Op,Press,Irr_dur" --timeformat "%Y-%m-%d %H:%M:%S"
    sleep $TIME_SECCONDS
done
