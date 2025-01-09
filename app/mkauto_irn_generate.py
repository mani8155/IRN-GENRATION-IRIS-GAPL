from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
import requests as req
import json
from django.contrib import messages
from .forms import *
import requests as req
import json

SECRET_KEY_API_URL = "https://api.meritplus.app/auth/token"
IRN_SECRET_KEY_VALUE = "5u65rGP8sU9R7KU7H1yDWevkTnjuNeT4"
CANCEL_IRN_SECRET_KEY_VALUE = "itpuuHctFNbAupXuWPksD11rBvbiRKXw"
QRCODE_SECRET_KEY_VALUE = "yX9NRwfIukMYQ5IVKBW81gibnRSbSgIR"


def mkauto_iris_from(request):
    apiurl = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

    payload = json.dumps({
        "psk_uid": "413f8b09-f538-4a8f-9c25-343bdfe17b78",
        "project": "",
        "data": {
            "fromdt": "2024-4-1",
            "todate": "2025-4-30"
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", apiurl, headers=headers, data=payload)

    if response.status_code != 200:
        return HttpResponse("The API for SQL views does not retrieve data")
    res_data = response.json()
    context = {"response_data": res_data}

    return render(request, 'mkauto/mk_iris_form.html', context)


def mkauto_iris_from_admin_view(request):
    apiurl = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

    payload = json.dumps({
        "psk_uid": "413f8b09-f538-4a8f-9c25-343bdfe17b78",
        "project": "",
        "data": {
            "fromdt": "2024-4-1",
            "todate": "2025-4-30"
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", apiurl, headers=headers, data=payload)
    if response.status_code != 200:
        return HttpResponse("The API for SQL views does not retrieve data")
    res_data = response.json()
    context = {"menu": "menu-mkauto", "response_data": res_data}

    return render(request, 'mkauto/mk_iris_form_admin.html', context)


def mkauto_generate_irn(request, inv_no):
    # print(inv_no)
    secretekey_api_url = f"{SECRET_KEY_API_URL}?secret_key={IRN_SECRET_KEY_VALUE}"
    payload = json.dumps({
        "secret_key": IRN_SECRET_KEY_VALUE
    })
    headers = {
        'Content-Type': 'application/json'
    }
    secretekey_response = req.request("POST", secretekey_api_url, headers=headers, data=payload)
    secretekey_response_data = secretekey_response.json()
    if secretekey_response.status_code != 200:
        messages.error(request, message="Sql Views secrete key invalid")

    token_value = secretekey_response_data['access_token']

    apiurl2 = "https://api.meritplus.app/coreapi/api/psm030001"

    payload = json.dumps({
        "data": {
            "itr_doc_id": inv_no
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token_value}'
    }

    response = req.request("POST", apiurl2, headers=headers, data=payload)
    # print(response.status_code)
    if response.status_code == 200:
        messages.success(request, message=response.json()['message'])
        return redirect('mkauto_iris_from')
    else:
        messages.error(request, message=response.text)
        return redirect('mkauto_iris_from')

def mkauto_cancel_irn_form(request, irn):
    # print(irn)
    return redirect('mkauto_cancel_irn', irn)

def mkauto_cancel_irn(request, irn):
    secretekey_api_url = f"{SECRET_KEY_API_URL}?secret_key={CANCEL_IRN_SECRET_KEY_VALUE}"
    payload = json.dumps({
        "secret_key": CANCEL_IRN_SECRET_KEY_VALUE
    })
    headers = {
        'Content-Type': 'application/json'
    }
    secretekey_response = req.request("POST", secretekey_api_url, headers=headers, data=payload)
    secretekey_response_data = secretekey_response.json()
    if secretekey_response.status_code != 200:
        messages.error(request, message="Sql views secrete key invalid")

    token_value = secretekey_response_data['access_token']

    apiurl2 = "https://api.meritplus.app/coreapi/api/psm030003"

    payload = json.dumps({
        "data": {
            "irn": irn
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token_value}'
    }

    response = req.request("POST", apiurl2, headers=headers, data=payload)
    if response.status_code == 200:
        messages.success(request, message=response.json()['message'])
        return redirect('mkauto_iris_from')
    else:
        messages.error(request, message=response.text)
        return redirect('mkauto_iris_from')


def mkauto_qr_code_generate(request, inv_no):
    secretekey_api_url = f"{SECRET_KEY_API_URL}?secret_key={QRCODE_SECRET_KEY_VALUE}"
    payload = json.dumps({
        "secret_key": QRCODE_SECRET_KEY_VALUE
    })
    headers = {
        'Content-Type': 'application/json'
    }
    secretekey_response = req.request("POST", secretekey_api_url, headers=headers, data=payload)
    secretekey_response_data = secretekey_response.json()
    if secretekey_response.status_code != 200:
        messages.error(request, message="Sql views secrete key invalid")

    token_value = secretekey_response_data['access_token']

    apiurl2 = "https://api.meritplus.app/coreapi/api/psm030004"

    payload = json.dumps({
        "data": {
            "itr_doc_id": inv_no
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token_value}'
    }

    response = req.request("POST", apiurl2, headers=headers, data=payload)
    # print(response.status_code)
    if response.status_code == 200:
        messages.success(request, message=response.json()['message'])
        return redirect('mkauto_iris_from_admin_view')
    else:
        messages.error(request, message=response.text)
        return redirect('mkauto_iris_from_admin_view')


# -----------------------------------------------------------------------

def mkauto_eway_bill_form(request, inv_no, doc_date, itr_id):
    # print(itr_id)
    if request.method == "POST":
        trn_mode = request.POST['trn_mode'].capitalize()
        transporter = request.POST['transporter']
        trn_gst = request.POST['trn_gst']
        trn_doc_no = request.POST['trn_doc_no']
        trn_date = request.POST['trn_date']
        trn_vec_no = request.POST['trn_vec_no']
        trn_vec_type = request.POST['trn_vec_type']

        url = "https://api.irisgst.com/irisgst/mgmt/login"

        payload = json.dumps({
            "email": "",
            "password": ""
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", url, headers=headers, data=payload)
        res_data = response.json()
        # print(res_data)
        nested_response = res_data['response']
        token_value = nested_response['token']
        # print(token_value)
        company_id = nested_response['companyid']
        # print(company_id)

        url = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

        payload = json.dumps({
            "psk_uid": "fdd0e2e9-8491-4ed7-8a37-bbe004d7b157",
            "project": "",
            "data": {
                "ITR_DocID": inv_no
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", url, headers=headers, data=payload)
        # print(response.json())
        irn_res = response.json()
        irn_value = irn_res[0]['irn']
        # print(type(irn_value))
        if irn_value == 'None':
            messages.error(request, message="IRN not generated. Please generate the IRN first.")
            return redirect('mkauto_iris_from')
        else:

            com_pincode = int(irn_res[0]['bpin'])
            buyer_pincode = int(irn_res[0]['spin'])

            url = "https://api.irisgst.com//irisgst/onyx/irn/generateEwbByIrn"

            payload = json.dumps({
                "userGstin": "33AABCG9414G1ZU",
                "transMode": trn_mode,
                "vehTyp": trn_vec_type,
                "transDist": 5 if com_pincode == buyer_pincode else 0,
                "subSplyTyp": "Supply",
                "subSplyDes": "",
                # "transName": "Safe and Secure",
                "transName": transporter,
                "transId": trn_gst,
                # "transId": "01ACQPN4602B002",
                "transDocNo": trn_doc_no,
                # "transDocDate": "24-04-2024",
                "transDocDate": str(trn_date),
                "vehNo": trn_vec_no,
                # "vehNo": "MH20ZZ8888",
                "irn": irn_value,
                # "irn": "cd90713760608f4b557af2f5ec4c30fea151b0d7d8cf3e15b9a8cd4b443540b2"
            })
            print(payload)
            headers = {
                'companyId': str(company_id),
                'X-Auth-Token': str(token_value),
                'product': 'ONYX',
                'Content-Type': 'application/json'
            }

            response = req.request("PUT", url, headers=headers, data=payload)
            iris_res = response.json()
            print(iris_res)

            if iris_res['status'] == "SUCCESS":
                nested_response = iris_res['response']
                EwbNo = nested_response['EwbNo']
                EwbDt = nested_response['EwbDt']
                EwbValidTill = nested_response['EwbValidTill']
                print(response.json())
                obj = GstIrnEwayBillLog(
                    api_einvoice_no=trn_doc_no,
                    api_ewaybill_no=EwbNo,
                    api_ewaybill_date=EwbDt,
                    api_ewaybill_validtill=EwbValidTill,
                    api_payload_ewaybill=json.dumps(payload, indent=2),
                    api_response_ewaybill=json.dumps(iris_res, indent=2),
                    api_status_message=iris_res['status']
                )
                obj.save()
                success_iris_res = {
                    "itr_id": itr_id,
                    "transportdocno": trn_doc_no,
                    "transportdocdate": doc_date,
                    "vehicleno": trn_vec_no,
                    "vehicletype": trn_vec_type,
                    "ewytransportmode": 306,
                    "transportid": None,
                    "transportname": transporter,
                    "transportgst": trn_gst,
                    "eway_res": response.json(),
                }
                # print(success_iris_res)

                GENRATE_EWAYBILL_COREAPI = "ItTafYTue190Hg6YqVnC9sRNffhXIIGE"

                sec_url = f"https://api.meritplus.app/auth/token?secret_key={GENRATE_EWAYBILL_COREAPI}"

                payload = ""
                headers = {}

                response = req.request("POST", sec_url, headers=headers, data=payload)

                sec_res = response.json()
                sec_res_token = sec_res['access_token']

                core_url = "https://api.meritplus.app/coreapi/api/psm030005"

                payload = json.dumps({
                    "data": success_iris_res
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {sec_res_token}'
                }

                response = req.request("POST", core_url, headers=headers, data=payload)

                if response.status_code == 200:
                    messages.success(request, message=response.json()['message'])
                    return redirect('mkauto_iris_from')
                else:
                    messages.error(request, message=response.text)

            else:
                messages.error(request, message=iris_res['errors'])
                obj = GstIrnEwayBillLog(
                    api_einvoice_no=trn_doc_no,
                    api_payload_ewaybill=json.dumps(payload, indent=2),
                    api_response_ewaybill=json.dumps(iris_res, indent=2),
                    api_status_message=iris_res['status']
                )
                obj.save()
                return redirect('mkauto_iris_from')

    context = {"invoice_no": inv_no, "doc_date": doc_date}
    return render(request, 'mkauto/mkauto_eway_bill_form.html', context)


def mkauto_eway_bill_form_admin(request, inv_no, doc_date, itr_id):
    # print(itr_id)
    if request.method == "POST":
        trn_mode = request.POST['trn_mode'].capitalize()
        transporter = request.POST['transporter']
        trn_gst = request.POST['trn_gst']
        trn_doc_no = request.POST['trn_doc_no']
        trn_date = request.POST['trn_date']
        trn_vec_no = request.POST['trn_vec_no']
        trn_vec_type = request.POST['trn_vec_type']

        url = "https://api.irisgst.com/irisgst/mgmt/login"

        payload = json.dumps({
            "email": "",
            "password": ""
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", url, headers=headers, data=payload)
        res_data = response.json()
        # print(res_data)
        nested_response = res_data['response']
        token_value = nested_response['token']
        # print(token_value)
        company_id = nested_response['companyid']
        # print(company_id)

        url = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

        payload = json.dumps({
            "psk_uid": "fdd0e2e9-8491-4ed7-8a37-bbe004d7b157",
            "project": "",
            "data": {
                "ITR_DocID": inv_no
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", url, headers=headers, data=payload)
        # print(response.json())
        irn_res = response.json()
        irn_value = irn_res[0]['irn']
        # print(type(irn_value))
        if irn_value == 'None':
            messages.error(request, message="IRN not generated. Please generate the IRN first.")
            return redirect('mkauto_iris_from')
        else:

            com_pincode = int(irn_res[0]['bpin'])
            buyer_pincode = int(irn_res[0]['spin'])
            url = "https://api.irisgst.com//irisgst/onyx/irn/generateEwbByIrn"

            payload = json.dumps({
                "userGstin": "33AABCG9414G1ZU",
                "transMode": trn_mode,
                "vehTyp": trn_vec_type,
                "transDist": 5 if com_pincode == buyer_pincode else 0,
                "subSplyTyp": "Supply",
                "subSplyDes": "",
                # "transName": "Safe and Secure",
                "transName": transporter,
                "transId": trn_gst,
                # "transId": "01ACQPN4602B002",
                "transDocNo": trn_doc_no,
                # "transDocDate": "24-04-2024",
                "transDocDate": str(trn_date),
                "vehNo": trn_vec_no,
                # "vehNo": "MH20ZZ8888",
                "irn": irn_value,
                # "irn": "cd90713760608f4b557af2f5ec4c30fea151b0d7d8cf3e15b9a8cd4b443540b2"
            })
            # print(payload)
            headers = {
                'companyId': str(company_id),
                'X-Auth-Token': str(token_value),
                'product': 'ONYX',
                'Content-Type': 'application/json'
            }

            response = req.request("PUT", url, headers=headers, data=payload)
            iris_res = response.json()
            # print(iris_res)

            if iris_res['status'] == "SUCCESS":
                nested_response = iris_res['response']
                EwbNo = nested_response['EwbNo']
                EwbDt = nested_response['EwbDt']
                EwbValidTill = nested_response['EwbValidTill']
                # print(response.json())
                obj = GstIrnEwayBillLog(
                    api_einvoice_no=trn_doc_no,
                    api_ewaybill_no=EwbNo,
                    api_ewaybill_date=EwbDt,
                    api_ewaybill_validtill=EwbValidTill,
                    api_payload_ewaybill=json.dumps(payload, indent=2),
                    api_response_ewaybill=json.dumps(iris_res, indent=2),
                    api_status_message=iris_res['status']
                )
                obj.save()
                success_iris_res = {
                    "itr_id": itr_id,
                    "transportdocno": trn_doc_no,
                    "transportdocdate": doc_date,
                    "vehicleno": trn_vec_no,
                    "vehicletype": trn_vec_type,
                    "ewytransportmode": 306,
                    "transportid": None,
                    "transportname": transporter,
                    "transportgst": trn_gst,
                    "eway_res": response.json(),
                }
                # print(success_iris_res)

                GENRATE_EWAYBILL_COREAPI = "ItTafYTue190Hg6YqVnC9sRNffhXIIGE"

                sec_url = f"https://api.meritplus.app/auth/token?secret_key={GENRATE_EWAYBILL_COREAPI}"

                payload = ""
                headers = {}

                response = req.request("POST", sec_url, headers=headers, data=payload)

                sec_res = response.json()
                sec_res_token = sec_res['access_token']

                core_url = "https://api.meritplus.app/coreapi/api/psm030005"

                payload = json.dumps({
                    "data": success_iris_res
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {sec_res_token}'
                }

                response = req.request("POST", core_url, headers=headers, data=payload)

                if response.status_code == 200:
                    messages.success(request, message=response.json()['message'])
                    return redirect('mkauto_iris_from')
                else:
                    messages.error(request, message=response.text)

            else:
                messages.error(request, message=iris_res['errors'])
                obj = GstIrnEwayBillLog(
                    api_einvoice_no=trn_doc_no,
                    api_payload_ewaybill=json.dumps(payload, indent=2),
                    api_response_ewaybill=json.dumps(iris_res, indent=2),
                    api_status_message=iris_res['status']
                )
                obj.save()
                return redirect('mkauto_iris_from')

    context = {"invoice_no": inv_no, "doc_date": doc_date}
    return render(request, 'mkauto/mkauto_eway_bill_form_admin.html', context)


def mkauto_transport_mode_jquery(request):
    if request.method == 'GET':
        trn_mode = request.GET.get('trn_mode', None)
        # print(trn_mode)

        if trn_mode is not None and trn_mode == "Road":

            url = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

            payload = json.dumps({
                "psk_uid": "f4817632-4db0-492a-bf35-3a1abe8963dc",
                "project": "",
                "data": {
                    "transporter_mode": trn_mode
                }
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = req.request("POST", url, headers=headers, data=payload)
            res_data = response.json()
            # print(res_data)
            transporters_names = []

            for data in res_data:
                transporters_names.append(data['PTY_Name'])

            # print(transporters_names)

            data = {
                'transporters_names': list(transporters_names)
            }
            return JsonResponse(data)
        else:
            # trn_mode parameter not found
            response_data = {
                'error': 'trn_mode parameter missing'
            }
            return JsonResponse(response_data, status=400)


def mkauto_transport_gst_jquery(request):
    if request.method == 'GET':
        trn_name = request.GET.get('trn_gst', None)
        # print(trn_name)
        apiurl = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

        payload = json.dumps({
            "psk_uid": "f4817632-4db0-492a-bf35-3a1abe8963dc",
            "project": "",
            "data": {
                "transporter_mode": "Road"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", apiurl, headers=headers, data=payload)
        transporters_names = response.json()
        # print(transporters_names)

        for trnname in transporters_names:
            if trnname['PTY_Name'] == trn_name:
                trans_gst = trnname['PTY_GSTNUMBER']
                return JsonResponse(data={"trans_gst": trans_gst})
            else:
                pass
