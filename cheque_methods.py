import json

import requests
from requests.auth import HTTPBasicAuth


def reg(phone, email='testmail@ndex.yan', name='Test user'):
    payload = {'email': email, 'name': name, 'phone': phone}
    data = requests.post('https://proverkacheka.nalog.ru:9999/v1/mobile/users/signup',
                         data=json.dumps(payload), headers={'Content-Type': 'application/json;charset=UTF-8',})
    if data.status_code != 204:
        raise ValueError(data.content.decode('utf-8'))
    return


def check_cheque(fn_number, fd_number, fpd_number, datetime, sum, cheque_type, number, code):
    url = 'https://proverkacheka.nalog.ru:9999/v1/ofds/*/inns/*/fss/' + str(fn_number) + '/operations/' \
          + str(cheque_type) + '/tickets/' + str(fd_number) + '?fiscalSign=' + str(fpd_number) + '&date=' \
          + str(datetime) + '&sum=' + str(sum)
    data = requests.get(url, auth=HTTPBasicAuth(number, code), headers={'device-id': '', 'device-os': 'Android 8.0'})
    if data.status_code == 204:
        return True
    return False


def get_cheque_data(fn_number, fd_number, fpd_number, number, code):
    url = 'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/' + str(fn_number) + '/tickets/' + str(fd_number) \
          + '?fiscalSign=' + str(fpd_number) + '&sendToEmail=no'
    data = requests.get(url, auth=HTTPBasicAuth(number, code), headers={'device-id': '', 'device-os': 'Android 8.0'})
    if data.status_code != 200:
        raise ValueError(data.content.decode('utf-8'))
    return json.loads(data.content.decode('utf-8'))['document']['receipt']
