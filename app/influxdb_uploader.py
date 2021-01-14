import csv
import datetime
import logging
import os
import re
import sys

import chardet
import pandas as pd
from influxdb import InfluxDBClient
from pytz import timezone

epoch_naive = datetime.datetime.utcfromtimestamp(0)
epoch = timezone('UTC').localize(epoch_naive)


def unix_time_millis(dt):
    return int((dt - epoch).total_seconds() * 1000)


def is_float(value):
    """
    Check if data type of field is float

    :param value: value to be checked
    :return: True if value is can be casted to float
    """

    try:
        float(value.replace(' ', '').replace(',', '.'))
        return True
    except:
        return False


def is_bool(value):
    """
    Check if data type of field is bool

    :param value: value to be checked
    :return: True if value is can be casted to bool
    """
    try:
        return value.lower() in ('true', 'false')
    except:
        return False


def str2bool(value):
    """
    Casts string to boolean

    :param value: value to be casted
    :return: True if string is 'True' in any case
    """
    return value.lower() == 'true'


def isinteger(value):
    """
    Check if data type of field is int

    :param value: value to be checked
    :return: True if value is can be casted to int
    """
    try:
        if float(value).is_integer():
            return True
        else:
            return False
    except:
        return False


def convert_to_csv(input_filename):
    """
    Open Excel file and transforms it to CSV

    :param input_filename: Excel file to convert to CSV
    """

    # with open(input_filename) as file:
    #     lines = file.readlines()
    #     for line in lines:
    #         print(line)
    read_file = pd.read_csv(input_filename, sep="\t")
    filename = "file_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M") + ".csv"
    read_file.to_csv(filename, index=None, sep=",")

    # with open('temp.csv', 'r', encoding='ISO-8859-1') as file_r, open(
    #         "file_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M") + ".csv", 'w') as file_w:
    #     for line in file_r:
    #         line = line.split(',')
    #         line[0] = re.sub("'", '', line[0])
    #         line = ','.join(line)
    #         file_w.write(line)

    # os.remove("temp.csv")
    return filename


def set_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def load_csv(input_filename, servername, user, password, dbname, metric,
             timecolumn, timeformat, tag_columns, field_columns,
             delimiter, batchsize, create, datatimezone, usessl):
    set_logger()

    host = servername[0:servername.rfind(':')]
    port = int(servername[servername.rfind(':') + 1:])
    client = InfluxDBClient(host, port, user, password, dbname, ssl=usessl)

    if create:
        logging.info('Deleting database %s' % dbname)
        client.drop_database(dbname)
        logging.info('Creating database %s' % dbname)
        client.create_database(dbname)

    client.switch_user(user, password)

    # format tags and fields
    if tag_columns:
        tag_columns = tag_columns.split(',')
    if field_columns:
        field_columns = field_columns.split(',')

    # open csv
    datapoints = []
    # input_file = "file_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M") + ".csv"
    input_filename = convert_to_csv(input_filename)
    # input_file = name
    # with open(input_file, 'rb') as file:
    #     encoding = chardet.detect(file.read())
    count = 0
    with open(input_filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            datetime_naive = datetime.datetime.strptime(row[timecolumn].replace("'", ''), timeformat)

            if datetime_naive.tzinfo is None:
                datetime_local = timezone(datatimezone).localize(datetime_naive)
            else:
                datetime_local = datetime_naive

            timestamp = unix_time_millis(datetime_local) * 1000000  # in nanoseconds

            tags = {}
            for t in tag_columns:
                v = 0
                if t in row:
                    v = row[t]
                tags[t] = v

            fields = {}
            for f in field_columns:
                v = 0
                if f in row:
                    if is_float(row[f]):
                        v = float(row[f].replace(' ', '').replace(',', '.'))
                    elif is_bool(row[f]):
                        v = str2bool(row[f])
                    else:
                        v = row[f]
                fields[f] = v

            point = {"measurement": metric, "time": timestamp, "fields": fields, "tags": tags}

            datapoints.append(point)
            count += 1

            if len(datapoints) % batchsize == 0:
                logging.info('Read %d lines' % count)
                logging.info('Inserting %d datapoints...' % (len(datapoints)))
                response = client.write_points(datapoints)

                if not response:
                    logging.error('Problem inserting points, exiting.')
                    exit(1)

                logging.info("Wrote %d points, up to %s, response: %s" % (len(datapoints), datetime_local, response))

                datapoints = []

    # write rest
    if len(datapoints) > 0:
        logging.info('Read %d lines' % count)
        logging.info('Inserting %d datapoints...' % (len(datapoints)))
        response = client.write_points(datapoints)

        if not response:
            logging.error('Problem inserting points, exiting...')
            exit(1)
        else:
            os.remove(input_filename)
        logging.info("Wrote %d, response: %s" % (len(datapoints), response))

    logging.info('Done')
