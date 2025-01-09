from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
import requests as req
import json
from django.contrib import messages
from .forms import *
import requests as req
import json


# Create your views here.

def company_form(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        api_url_value = request.POST['api_url']
        api_type = request.POST['api_type']

        # email = "srikanth@b2e.in"
        # password = "B2e@1234#"
        # api_url_value = "https://stage-api.irisgst.com/irisgst/mgmt/login"
        # api_type = "development"

        # print(api_url_value, api_type, email, password)
        api_url = api_url_value

        # print(api_url)

        payload = json.dumps({
            "email": email,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", api_url, headers=headers, data=payload)
        # print(response.text)
        if response.status_code == 200:
            response_json = response.json()

            if response_json.get("status") == "SUCCESS":
                nested_response = response_json['response']
                companyName = nested_response['rootCompanyName']
                companyid = nested_response['companyid']
                tokenValue = nested_response['token']

                api_response = json.dumps(nested_response, indent=4)

                exis_obj = Company.objects.filter(email=email, api_type=api_type).first()
                # exis_obj = Company.objects.get(email=email, api_type=api_type)

                if exis_obj:
                    print("dmfnvmfn")
                    exis_obj.email = email,
                    exis_obj.password = password,
                    exis_obj.company_name = companyName,
                    exis_obj.company_id = companyid,
                    exis_obj.token = tokenValue,
                    exis_obj.api_response = api_response,
                    exis_obj.api_url = api_url,
                    exis_obj.api_type = api_type
                    exis_obj.save()
                    messages.success(request, message=f"updated existing data.")
                    return redirect('empanelled_irps_list')
                else:

                    obj = Company.objects.create(
                        email=email,
                        password=password,
                        company_name=companyName,
                        company_id=companyid,
                        token=tokenValue,
                        api_response=api_response,
                        api_url=api_url,
                        api_type=api_type
                    )
                    messages.success(request, "Login success")
                    return redirect('empanelled_irps_list')

            else:
                messages.error(request, message=response_json.get("message", "Invalid credentials"))
        else:
            messages.error(request, message="Api time out")

    # return render(request, 'form.html')
    return render(request, 'auth-login.html')


def forgot_password(request):
    if request.method == "POST":
        api_type = request.POST['api_type']
        email = request.POST['email']
        current_password = request.POST['current_password']
        newpassword = request.POST['newpassword']
        # print(email, current_password, newpassword)

        apiurl = "https://stage-api.irisgst.com/irisgst/mgmt/public/user/changepassword"

        payload = json.dumps({
            "curentpassword": current_password,
            "newpassword": newpassword,
            "confirmpassword": newpassword,
            "changePasswordFromLogin": True,
            "email": email
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", apiurl, headers=headers, data=payload)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("status") == "SUCCESS":
                nested_response = response_json['response']
                obj = Company.objects.get(email=email, api_type=api_type)
                # print(obj)
                obj.password = newpassword
                obj.token = nested_response['X-Auth-Token']
                obj.save()
                messages.success(request, message=response_json.get("message"))
                return redirect('company_form')
            else:
                messages.error(request, message=response_json.get("message"))

    return render(request, 'forgot-password.html')


def empanelled_irps_list(request):
    objs = EmpanelledIrps.objects.all()
    context = {"menu": "menu-emp-list", "obj": objs}
    return render(request, 'empanelled/empanelled_irps_list.html', context)


def empanelled_irps_form(request):
    form_type = "Create Empanelled Form"
    form = EmpanelledIrpsForm()

    if request.method == "POST":
        form = EmpanelledIrpsForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            messages.success(request, "Created Successfully")
            return redirect('empanelled_irps_list')

    context = {
        "menu": "menu-emp-list",
        "form": form,
        "form_type": form_type
    }
    return render(request, 'empanelled/empanelled_irps_form.html', context)


def edit_empanelled_irps(request, id):
    form_type = "Edit Empanelled Form"
    obj = EmpanelledIrps.objects.get(id=id)

    form = EmpanelledIrpsForm(instance=obj)

    if request.method == "POST":
        form = EmpanelledIrpsForm(request.POST, instance=obj)

        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect('empanelled_irps_list')

    context = {
        "menu": "menu-emp-list",
        "form": form,
        "form_type": form_type
    }
    return render(request, 'empanelled/empanelled_irps_form.html', context)


def auth_login(request):
    obj = EmpanelledIrps.objects.values_list('irp_name', flat=True).distinct()

    if request.method == 'POST':
        irp_name = request.POST['irp_name']
        email = request.POST['email']
        password = request.POST['password']
        api_url_value = request.POST['api_url']

        # print(irp_name, email, password, api_url_value)

        obj2 = EmpanelledIrps.objects.get(url_link=api_url_value)
        api_type = obj2.url_type

        api_url = api_url_value

        # print(api_url)

        payload = json.dumps({
            "email": email,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", api_url, headers=headers, data=payload)
        # print(response.text)
        if response.status_code == 200:
            response_json = response.json()

            if response_json.get("status") == "SUCCESS":
                nested_response = response_json['response']
                companyName = nested_response['rootCompanyName']
                companyid = nested_response['companyid']
                tokenValue = nested_response['token']

                api_response = json.dumps(nested_response, indent=4)

                exis_obj = Company.objects.filter(email=email, api_type=api_type).first()
                # exis_obj = Company.objects.get(email=email, api_type=api_type)

                if exis_obj:
                    exis_obj.email = email,
                    exis_obj.password = password,
                    exis_obj.company_name = companyName,
                    exis_obj.company_id = companyid,
                    exis_obj.token = tokenValue,
                    exis_obj.api_response = api_response,
                    exis_obj.api_url = api_url,
                    exis_obj.api_type = api_type
                    exis_obj.irp_name = irp_name
                    messages.success(request, message=f"updated existing data.")
                    return redirect('empanelled_irps_list')
                else:

                    obj = Company.objects.create(
                        email=email,
                        password=password,
                        company_name=companyName,
                        company_id=companyid,
                        token=tokenValue,
                        api_response=api_response,
                        api_url=api_url,
                        api_type=api_type,
                        irp_name=irp_name
                    )
                    messages.success(request, "Login success")
                    return redirect('empanelled_irps_list')

            else:
                messages.error(request, message=response_json.get("message", "Invalid credentials"))
        else:
            messages.error(request, message="Api time out")

    context = {
        "menu": "menu-emp-list",
        "empanelled_irps": obj

    }
    return render(request, 'auth_login2.html', context)


def auth_login_admin(request):
    obj = EmpanelledIrps.objects.values_list('irp_name', flat=True).distinct()

    if request.method == 'POST':
        irp_name = request.POST['irp_name']
        email = request.POST['email']
        password = request.POST['password']
        api_url_value = request.POST['api_url']
        user_gstin = request.POST['user_gstin']
        # print(user_gstin)

        # print(irp_name, email, password, api_url_value)

        obj2 = EmpanelledIrps.objects.get(url_link=api_url_value)
        api_type = obj2.url_type

        api_url = api_url_value

        # print(api_url)

        payload = json.dumps({
            "email": email,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", api_url, headers=headers, data=payload)
        # print(response.text)
        if response.status_code == 200:
            response_json = response.json()

            if response_json.get("status") == "SUCCESS":
                nested_response = response_json['response']
                companyName = nested_response['rootCompanyName']
                companyid = nested_response['companyid']
                tokenValue = nested_response['token']

                api_response = json.dumps(nested_response, indent=4)

                exis_obj = Company.objects.filter(email=email, api_type=api_type).first()
                # exis_obj = Company.objects.get(email=email, api_type=api_type)

                if exis_obj:
                    exis_obj.user_gstin = user_gstin
                    exis_obj.email = email
                    exis_obj.password = password
                    exis_obj.save()
                    messages.success(request, message=f"updated existing data.")
                    return redirect('company_list')
                else:

                    obj = Company.objects.create(
                        email=email,
                        password=password,
                        company_name=companyName,
                        company_id=companyid,
                        token=tokenValue,
                        api_response=api_response,
                        api_url=api_url,
                        api_type=api_type,
                        irp_name=irp_name,
                        user_gstin=user_gstin
                    )
                    messages.success(request, "Created successfully")
                    return redirect('company_list')

            else:
                messages.error(request, message=response_json.get("message", "Invalid credentials"))
        else:
            messages.error(request, message="Api time out")

    context = {
        "menu": "menu-com",
        "empanelled_irps": obj

    }
    return render(request, 'company/admin/auth_login2.html', context)


def get_api_urls(request):
    if request.method == 'GET':
        irp_name = request.GET.get('irpName')
        # print(irp_name)
        obj = EmpanelledIrps.objects.filter(irp_name=irp_name)
        api_urls = [irp.url_link for irp in obj]
        # print(api_urls)

        data = {
            "api_urls": api_urls
        }

        return JsonResponse(data)


def iris_from(request):
    apiurl = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

    payload = json.dumps({
        "psk_uid": "56eb9f0b-ba0b-4a98-a8f7-68b6f9a2c24a",
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

    # print(transporters_names)

    context = {"response_data": res_data}

    return render(request, 'iris/iris_form.html', context)


def company_list(request):
    obj = Company.objects.all()
    context = {"menu": "menu-com", "all_data": obj}
    return render(request, 'company/company_list.html', context)


def generate_irn_admin_view(request):
    apiurl = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

    payload = json.dumps({
        "psk_uid": "56eb9f0b-ba0b-4a98-a8f7-68b6f9a2c24a",
        "project": "",
        "data": {
            "fromdt": "2024-4-1",
            "todate": "2024-4-30"
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", apiurl, headers=headers, data=payload)
    res_data = response.json()
    context = {"response_data": res_data, "menu": "menu-irn"}

    return render(request, 'iris/admin/iris_form.html', context)


SECRET_KEY_API_URL = "https://api.meritplus.app/auth/token"
SECRET_KEY_VALUE = "C0QdNkHE0hngTubOJKaUGSylbcptsrH2"
CANCEL_IRN_SECRET_KEY_VALUE = "WK06DMBY83lVsDUlAQuw0aAJE7J5dLyv"


def generate_irn(request, inv_no):
    # print(inv_no)
    secretekey_api_url = f"{SECRET_KEY_API_URL}?secret_key={SECRET_KEY_VALUE}"
    payload = json.dumps({
        "secret_key": SECRET_KEY_VALUE
    })
    headers = {
        'Content-Type': 'application/json'
    }
    secretekey_response = req.request("POST", secretekey_api_url, headers=headers, data=payload)
    secretekey_response_data = secretekey_response.json()
    if secretekey_response.status_code != 200:
        messages.error(request, message="Sql views secrete key invalid")

    token_value = secretekey_response_data['access_token']

    apiurl2 = "https://api.meritplus.app/coreapi/api/fin042002"

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
    print(response.text)
    # print(response.status_code)
    if response.status_code == 200:
        messages.success(request, message=response.json()['message'])
        return redirect('labour_invoice_form')
        # return redirect('iris_from')
    else:
        messages.error(request, message=response.text)
        return redirect('labour_invoice_form')
        # return redirect('iris_from')


def cancel_irn_form(request, irn):
    # print(irn)
    return redirect('cancel_irn', irn)


def cancel_irn(request, irn):
    secretekey_api_url = f"{SECRET_KEY_API_URL}?secret_key={CANCEL_IRN_SECRET_KEY_VALUE}"
    payload = json.dumps({
        "secret_key": SECRET_KEY_VALUE
    })
    headers = {
        'Content-Type': 'application/json'
    }
    secretekey_response = req.request("POST", secretekey_api_url, headers=headers, data=payload)
    secretekey_response_data = secretekey_response.json()
    if secretekey_response.status_code != 200:
        messages.error(request, message="Sql views secrete key invalid")

    token_value = secretekey_response_data['access_token']

    apiurl2 = "https://api.meritplus.app/coreapi/api/fin042003"

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
        return redirect('iris_from')
    else:
        messages.error(request, message=response.text)
        return redirect('iris_from')


def eway_bill_form(request, inv_no, doc_date, itr_id):
    # print(itr_id)
    if request.method == "POST":
        trn_mode = request.POST['trn_mode'].capitalize()
        transporter = request.POST['transporter']
        trn_gst = request.POST['trn_gst']
        trn_doc_no = request.POST['trn_doc_no']
        trn_date = request.POST['trn_date']
        trn_vec_no = request.POST['trn_vec_no']
        trn_vec_type = request.POST['trn_vec_type']

        print(transporter, trn_gst)

        url = "https://stage-api.irisgst.com/irisgst/mgmt/login"

        payload = json.dumps({
            "email": "srikanth@b2e.in",
            "password": "B2e@1234#"
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
            "psk_uid": "c22ec565-e8be-4fbf-b229-007228130f7e",
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
            return redirect('iris_from')
        else:
            # print("IRN Prensent")
            # print(irn_value)

            url = "https://stage-api.irisgst.com//irisgst/onyx/irn/generateEwbByIrn"

            payload = json.dumps({
                "userGstin": "33AAACI9260R002",
                "transMode": trn_mode,
                "vehTyp": trn_vec_type,
                "transDist": 0,
                "subSplyTyp": "Supply",
                "subSplyDes": "",
                "transName": "Safe and Secure",
                # "transName": transporter,
                # "transId": trn_gst,
                "transId": "01ACQPN4602B002",
                "transDocNo": trn_doc_no,
                "transDocDate": "24-04-2024",
                # "transDocDate": str(trn_date),
                # "vehNo": trn_vec_no,
                "vehNo": "MH20ZZ8888",
                # "irn": irn_value,
                "irn": "a9260321af2fa5624afdbf4f4338205bdc86a54ee4f2c7d1c2ebef794cc86696"
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

                sec_url = "https://api.meritplus.app/auth/token?secret_key=r7AcoUMaqzJEyggkyL3T4VnVhB9PqLlb"

                payload = ""
                headers = {}

                response = req.request("POST", sec_url, headers=headers, data=payload)

                sec_res = response.json()
                sec_res_token = sec_res['access_token']

                # core_url = "http://127.0.0.1:8007/coreapi/api/tst01qwerty"
                core_url = "https://api.meritplus.app/coreapi/api/psm040002"

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
                    return redirect('iris_from')
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
                return redirect('iris_from')

    context = {"invoice_no": inv_no, "doc_date": doc_date}
    return render(request, 'iris/eway_bill_form.html', context)


def transport_mode_jquery(request):
    if request.method == 'GET':
        trn_mode = request.GET.get('trn_mode', None)
        # print(trn_mode)

        if trn_mode is not None and trn_mode == "Road":

            url = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

            payload = json.dumps({
                "psk_uid": "84055c85-2134-4df2-862a-b5693eec1c7f",
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


def transport_gst_jquery(request):
    if request.method == 'GET':
        trn_name = request.GET.get('trn_gst', None)
        # print(trn_name)
        apiurl = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

        payload = json.dumps({
            "psk_uid": "84055c85-2134-4df2-862a-b5693eec1c7f",
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


# --------------------- Labour Invoice -------------------

def labour_invoice_form(request):
    apiurl = "https://api.meritplus.app/sqlviews/api/v1/get_respone_data"

    payload = json.dumps({
        "psk_uid": "b766d50c-c67b-499f-88c1-5b3b516146ce",
        "project": "",
        "data": {
            "fromdt": "2024-4-1",
            "todate": "2024-5-1"
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", apiurl, headers=headers, data=payload)
    if response.status_code != 200:
        return HttpResponse("The API for SQL views does not retrieve data")
    res_data = response.json()

    # print(transporters_names)

    context = {"response_data": res_data}

    return render(request, 'labour/labour_invoice_form.html', context)
