import configparser
import requests
import csv
import os

home = os.path.expanduser('~/')
config = configparser.ConfigParser()
config.read(f'{home}key_vault.config')

headers = {
'Authorization': config['SMARTSHEET']['api-key'],
'Content-Type': 'application/json',
}

users_to_remove = []
def read_smartsheet_csv():
    with open('smartsheet_users.csv', 'r') as smartsheet_users:
        reader = csv.reader(smartsheet_users)
        next(reader)
        for row in reader:
            users_to_remove.append(row)
            smartsheet_ids(row[0])

def smartsheet_ids(row):
    params = (
        ('email', '{}'.format(row)),
        ('include', 'lastLogin'),
    ) 

    response = requests.get('https://api.smartsheet.com/2.0/users', headers=headers, params=params)
    data = response.json()
    remove_licence(data['data'][0]['id'])

def remove_licence(row):
    data = '{"admin": false, "licensedSheetCreator": false}'
    response = requests.put('https://api.smartsheet.com/2.0/users/{}'.format(row), headers=headers, data=data)
    data = response.json()
    print (data['message'], '\nname:', data['result']['email'], '\nlicense_status:', data['result']['licensedSheetCreator'], '\n')


read_smartsheet_csv()
