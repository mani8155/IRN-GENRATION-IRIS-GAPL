from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .forms import *
import requests as req
import json

SQL_VIEWS_API_URL = "http://127.0.0.1:8009/"
CORE_API_URL = "http://127.0.0.1:8007/"
AUTH_URL = "http://127.0.0.1:8011/"

IRIS_AUTH_LOGIN_URL = "https://stage-api.irisgst.com/irisgst/mgmt/login"
STAGE_IRIS_URL = "https://stage-api.irisgst.com/"

# IRIS_AUTH_LOGIN_URL = "https://api.irisgst.com/irisgst/mgmt/login"
PRODUCTION_IRIS_URL = "https://api.irisgst.com/"

GENERATE_IRN_CORE_API_SECRETE_KEY = "WyVVgiwqmBP9mz7tfEgVbihcDdwv3EcU"

CANCEL_IRN_CORE_API_SECRETE_KEY = "PeaR0dxqK6ScqrEx85InklKHMLquo4ci"

UserGSTIN = "33AAACI9260R002"


# UserGSTIN = "33AABCG9414G1ZU"


def gapl_credit_note_screen(request):
    credit_url = f"{SQL_VIEWS_API_URL}sqlviews/api/v1/get_respone_data"
    payload = json.dumps({
        "psk_uid": "ab512fdd-a21f-4661-af4b-567981852c1f",
        "project": "",
        "data": {
            "fromdate": "2024-05-01",
            "todate": "2025-05-31"
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", credit_url, headers=headers, data=payload)

    if response.status_code != 200:
        messages.error(request, message="This API does not receive data for sql views 'gapl_credit_note_screen'.")

    context = {
        "response_data": response.json()
    }

    return render(request, 'gapl_credit/gapl_credit_note_screen.html', context)


def gapl_company_data(request):
    url = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

    payload = json.dumps({
        "psk_uid": "9c7152ec-5e5d-4474-b7d9-c2f462e487a7",
        "project": "gstin",
        "data": {}
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        messages.error("Not working in SQLViews is the Gapl company data api call.")

    res = response.json()
    com_res = res[0]

    email = com_res['email']
    password = com_res['password']

    return email, password


def iris_login(request):
    email, password = gapl_company_data(request)
    aut_url = IRIS_AUTH_LOGIN_URL
    # GaplEmail, GaplPassword = gapl_company_data(request)

    GaplEmail, GaplPassword = "srikanth@b2e.in", "B2e@9999#"

    payload = json.dumps({
        "email": GaplEmail,
        "password": GaplPassword
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", aut_url, headers=headers, data=payload)
    auth_res = response.json()

    if response.status_code == 200:
        response_json = response.json()
        auth_resonse_data = auth_res['response']
        auth_token = auth_resonse_data['token']
        company_id = auth_resonse_data['companyid']
        return company_id, auth_token

    else:
        messages.error(request, message="IRIS Login Credential Wrong")
        return redirect('gapl_credit_note_screen')


def coreapi_secrete_key(request):
    url = f"{AUTH_URL}auth/token?secret_key={GENERATE_IRN_CORE_API_SECRETE_KEY}"

    payload = {}
    headers = {}

    response = req.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        messages.error(request, message="Core Secrete Key API Not Working")
        return redirect('gapl_credit_note_screen')

    res_data = response.json()

    access_token = res_data['access_token']
    return access_token


def iris_api_call(request, payload, company_id, auth_token):
    iris_url = f"{STAGE_IRIS_URL}irisgst/onyx/irn/addInvoice"
    # iris_url = f"{PRODUCTION_IRIS_URL}irisgst/onyx/irn/addInvoice"

    payload = payload
    headers = {
        'companyId': str(company_id),
        'X-Auth-Token': f"{str(auth_token)}",
        'product': 'ONYX',
        'Content-Type': 'application/json'
    }

    iris_response = req.request("POST", iris_url, headers=headers, data=payload)

    iris_res = iris_response.json()
    if iris_res['status'] == "SUCCESS":
        print(payload)
        response_data = iris_res['response']
        irn = response_data['irn']
        return irn
    else:
        print(f"Error payload : {payload}")
        print(iris_res)
        print(iris_res.get('errors')[0])
        # messages.error(request, message=f"{iris_res.get('message')}")
        # return redirect('gapl_credit_note_screen')
        irn = iris_res.get('errors')[0]
        return irn

    # print(iris_response.text)


def core_api_integrate(request, irn, credit_note_no):
    # print(irn)
    core_api_secreteKeyTokenValue = coreapi_secrete_key(request)

    core_url = "http://127.0.0.1:8007/coreapi/api/psm030001"

    core_payload = json.dumps({
        "data": {
            "credit_note_no": credit_note_no,
            "irn": irn
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {core_api_secreteKeyTokenValue}'
    }

    core_response = req.request("POST", core_url, headers=headers, data=core_payload)

    if core_response.status_code == 200:
        core_response_data = core_response.json()
        messages.success(request, message=core_response_data['message'])
        return redirect('gapl_credit_note_screen')
    else:
        messages.error(request, message="IRN generated fail")
        return redirect('gapl_credit_note_screen')


def gapl_credit_irn_generate(request, credit_note_no: str):
    sql_views_url = f"{SQL_VIEWS_API_URL}sqlviews/api/v1/get_respone_data"

    payload = json.dumps({
        "psk_uid": "44ad856c-bc6f-445f-8299-e24b68454322",
        "project": "",
        "data": {
            "DOCID": credit_note_no
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    sql_views_response = req.request("POST", sql_views_url, headers=headers, data=payload)

    if sql_views_response.status_code != 200:
        messages.error(request, message="SqlViews: credit_note_no against data retrieve api call not working")
        return redirect('gapl_credit_note_screen')

    sql_views_payload = sql_views_response.json()

    item_list = ["unitPrice", "sval", "txval", "hsnCd", "itmVal", "qty", "camt", "crt",
                 "prdDesc", "prdNm", "rt", "samt", "srt", "txp", "unit", "irt"]

    # print(json.dumps(common_data))

    data = []
    num_format = "{:05d}"  # Format for numbering with leading zeros
    num_counter = 1  # Starting number

    for item in sql_views_payload:
        # print(item)
        _item = {"num": num_format.format(num_counter)}
        for i in item_list:
            try:
                if i == "qty":
                    _item[i] = int(float(item[i]))
                elif i == "unitPrice":
                    _item[i] = float(item[i])
                elif i == "sval":
                    _item[i] = float(item[i])
                elif i == "txval":
                    _item[i] = float(item[i])
                elif i == "camt":
                    _item[i] = float(item[i])
                elif i == "samt":
                    _item[i] = float(item[i])
                elif i == "rt":
                    _item[i] = int(float(item[i]))
                elif i == "crt":
                    _item[i] = int(float(item[i]))
                elif i == "srt":
                    _item[i] = int(float(item[i]))
                elif i == "itmVal":
                    _item[i] = int(float(item[i]))
                elif i == "irt":
                    _item[i] = int(float(item[i]))
                else:
                    _item[i] = item[i]
            except KeyError:
                pass
        data.append(_item)
        num_counter += 1  # Increment the counter

    # print(data)

    # print(json.dumps(data))  # Or do whatever you want with the resulting data

    common_data = sql_views_payload[0]
    common_data.pop("tname")
    # common_data.pop("totiamt")

    for i in item_list:
        common_data.pop(i)

    common_data['itemList'] = data

    # print(common_data)

    common_data['sph'] = int(float(common_data['sph']))
    common_data['totinvval'] = int(float(common_data['totinvval']))
    common_data['tottxval'] = float(common_data['tottxval'])
    common_data['totcamt'] = float(common_data['totcamt'])
    common_data['totsamt'] = float(common_data['totsamt'])
    common_data['sflno'] = None
    common_data['bflno'] = None
    # common_data['sstcd'] = "33"
    # common_data['bstcd'] = "33"
    # common_data['pos'] = "33"
    common_data['dt'] = "13-04-2024"
    common_data['userGstin'] = "33AAACI9260R002"
    common_data['sgstin'] = "33AAACI9260R002"

    # buyer deatils
    common_data['bgstin'] = "30AAACI9260R002"
    common_data['bstcd'] = "30"
    common_data['bpin'] = "403802"
    value = float(common_data["totiamt"])
    common_data["totiamt"] = round(value, 2)

    payload = json.dumps(common_data)
    # print(payload)
    company_id, auth_token = iris_login(request)
    irn = iris_api_call(request, payload, company_id, auth_token)

    print(type(irn))
    if isinstance(irn, dict):
        print("irn is a dictionary")
        messages.error(request, message=irn)
        return redirect('gapl_credit_note_screen')

    response = core_api_integrate(request, irn, credit_note_no)
    if not response:
        messages.error(request, "Unexpected error occurred")
        return redirect('gapl_credit_note_screen')
    return response



#-------------------------------------------------------------------------

def iris_cancel_credit(request, irn, status_value):
    company_id, auth_token = iris_login(request)
    payload = json.dumps({
        "irn": irn,
        "cnlRsn": "1",
        "cnlRem": status_value,
        "userGstin": UserGSTIN
    })

    iris_url = f"{STAGE_IRIS_URL}irisgst/onyx/irn/cancel"
    # iris_url = f"{PRODUCTION_IRIS_URL}irisgst/onyx/irn/cancel"

    payload = payload
    headers = {
        'companyId': str(company_id),
        'X-Auth-Token': f"{str(auth_token)}",
        'product': 'ONYX',
        'Content-Type': 'application/json'
    }

    iris_response = req.request("PUT", iris_url, headers=headers, data=payload)

    iris_res = iris_response.json()
    print(iris_res)
    if iris_res['status'] == "SUCCESS":
        status = iris_res['status']
        return status
    else:
        status = "FAILURE"
        return status


def gapl_coreapi_cancel_irn(request):
    url = f"{AUTH_URL}auth/token?secret_key={CANCEL_IRN_CORE_API_SECRETE_KEY}"

    payload = {}
    headers = {}

    response = req.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        messages.error(request, message="Core Secrete Key API Not Working")
        return redirect('gapl_credit_note_screen')

    res_data = response.json()

    access_token = res_data['access_token']
    return access_token


def gapl_cancel_irn_core_api_integrate(request, credit_note_no):
    # print(irn)
    core_api_secreteKeyTokenValue = gapl_coreapi_cancel_irn(request)

    core_url = "http://127.0.0.1:8007/coreapi/api/psm04002"

    core_payload = json.dumps({
        "data": {
            "credit_note_no": credit_note_no,
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {core_api_secreteKeyTokenValue}'
    }

    core_response = req.request("POST", core_url, headers=headers, data=core_payload)

    if core_response.status_code == 200:
        core_response_data = core_response.json()
        messages.success(request, message=core_response_data['message'])
        return redirect('gapl_credit_note_screen')
    else:
        messages.error(request, message="IRN Canceled Fail")
        return redirect('gapl_credit_note_screen')


def gapl_credit_cancel(request, irn, credit_note_no):
    if request.method == "POST":
        status_value = request.POST['status_value']
        response = iris_cancel_credit(request, irn, status_value)

        if response != "SUCCESS":
            messages.error(request, message="IRN Cancelled Failed")
            return redirect('gapl_credit_note_screen')

        response = gapl_cancel_irn_core_api_integrate(request, credit_note_no)
        if not response:
            messages.error(request, "Unexpected error occurred")
            return redirect('gapl_credit_note_screen')
        return response
