from flask import Flask, render_template, request, make_response, redirect

from cheque_methods import check_cheque, get_cheque_data, reg
from geo_decoder import get_coords

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    phone = request.form['phone']
    code = request.form['code']
    if code == '':
        reg(phone)
        return render_template('login.html', phone=phone, message='sms has send')
    else:
        resp = make_response(redirect('/cheque'))
        resp.set_cookie('phone', phone)
        resp.set_cookie('code', code)
        return resp


@app.route('/cheque', methods=['GET', 'POST'])
def cheque():
    code = request.cookies.get('code') or 'none'
    phone = request.cookies.get('phone') or 'none'
    if request.method == 'POST':
        params = {'phone': phone, 'code': code, 'fn': request.form['fn'] or '', 'fd': request.form['fd'] or '',
                  'fdp': request.form['fdp'] or '', 'datetime': request.form['datetime'] or '',
                  'sum': request.form['sum'] or ''}
        params['exists'] = 'yes' if check_cheque(params['fn'], params['fd'], params['fdp'], params['datetime'],
                                                 params['sum'], request.form['type'], phone, code) else 'no'
        params['cheque_info'] = get_cheque_data(params['fn'], params['fd'], params['fdp'], phone, code)
        params['cheque_info']['coords'] = get_coords(params['cheque_info']['retailPlaceAddress'])
    else:
        params = {'phone': phone, 'code': code, 'fn': '', 'fd': '', 'fdp': '', 'datetime': '', 'sum': '',
                  'exists': 'None', 'cheque_info': '', 'coords': ''}
    return render_template('cheque.html', **params)
