import requests
import json
import boto3
from decimal import Decimal
import time
import datetime
from boto3.dynamodb.conditions import Key

params = {
  'api_key': '65c7da93-36b1-4dab-8a42-ea4b4cab9a0e',
  'dep_iata': 'LAS',
  '_fields': 'dep_iata,arr_iata,airline_iata,flight_number,status,dep_time,duration,dep_terminal,dep_gate,delayed'
}
method = 'schedules'
api_base = 'http://airlabs.co/api/v9/'

def listflights():
    api_result = requests.get(api_base+method, params)
    api_response = api_result.json()['response']

    print(json.dumps(api_response, indent=4, sort_keys=True))

    with open('/tmp/data.json', 'w', encoding='utf-8') as f:
        json.dump(api_response, f, ensure_ascii=False, indent=4)


def loadflights(flights, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Flights')
    nb = 0
    with table.batch_writer() as batch:
        for flight in flights:
            nb += 1
            airline_iata = flight['airline_iata']
            arr_iata = flight['arr_iata']
            delayed = flight['delayed']
            dep_gate = flight['dep_gate']
            dep_iata = flight['dep_iata']
            dep_terminal = flight['dep_terminal']
            dep_time = flight['dep_time']
            flight_number = flight['flight_number']
            status = flight['status']
            print('nb: ', nb)
            print("Adding flight:", arr_iata, flight_number)
            try:
                putres = batch.put_item(Item=flight)
                print('putres: ', putres)
            except Exception as e:
                print('error in put item: ', e)
            time.sleep(0.3)


def scanflights(dest, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Flights')
    response = table.query(
        KeyConditionExpression=Key('arr_iata').eq(dest)
    )

    for scan in response['Items']:
        format = '%Y-%m-%d %H:%M'
        datetimer = datetime.datetime.strptime(scan['dep_time'], format)
        currenttime = int(time.time())-10800
        difftime = datetimer.timestamp() - currenttime

        takeoffin = int(difftime / 60)

        if 0 < difftime < 36000:
            nextflight = "THE NEXT FLIGHT TO %s leaves in %s minutes. Flight number is %s at %s and leaves from terminal %s gate %s" %(scan['arr_iata'], takeoffin, scan['flight_number'], scan['dep_time'], scan['dep_terminal'], scan['dep_gate'])

            return nextflight


def handler_name(event, context): 
    listflights()

    with open("/tmp/data.json") as json_file:
        flight_list = json.load(json_file, parse_float=Decimal)
    loadflights(flight_list)