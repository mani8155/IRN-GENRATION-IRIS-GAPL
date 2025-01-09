from django.urls import path
from .views import *
from .gapl_irn_generate import *
from .mkauto_irn_generate import *
from .gapl_credit_note import *
from .gapl_debit_note import *

urlpatterns = [
    path('company_form/', company_form, name="company_form"),
    path('forgot_password/', forgot_password, name="forgot_password"),

    path('auth_login/', auth_login, name="auth_login"),
    path('auth_login_admin/', auth_login_admin, name="auth_login_admin"),
    path('get_api_urls/', get_api_urls, name="get_api_urls"),
    path('company_list/', company_list, name="company_list"),

    path('generate_irn_admin_view/', generate_irn_admin_view, name="generate_irn_admin_view"),
    path('generate_irn/<str:inv_no>/', generate_irn, name="generate_irn"),
    path('cancel_irn/<str:irn>/', cancel_irn, name="cancel_irn"),
    path('cancel_irn_form/<str:irn>/', cancel_irn_form, name="cancel_irn_form"),

    path('iris_form/', iris_from, name="iris_from"),
    path('eway_bill_form/<str:inv_no>/<str:doc_date>/<int:itr_id>/', eway_bill_form, name="eway_bill_form"),
    path('transport_mode_jquery/', transport_mode_jquery, name="transport_mode_jquery"),
    path('transport_gst_jquery/', transport_gst_jquery, name="transport_gst_jquery"),

    # ---------------------- Empanelled --------------------------------

    path('', empanelled_irps_list, name="empanelled_irps_list"),
    path('empanelled_irps_form/', empanelled_irps_form, name="empanelled_irps_form"),
    path('edit_empanelled_irps/<int:id>/', edit_empanelled_irps, name="edit_empanelled_irps"),

    # --------------------------- GAPL ---------------------------------------------

    path('gapl_iris_form/', gapl_iris_from, name="gapl_iris_from"),
    path('gapl_iris_from_admin_view/', gapl_iris_from_admin_view, name="gapl_iris_from_admin_view"),
    path('gapl_qr_code_generate/<str:inv_no>/', gapl_qr_code_generate, name="gapl_qr_code_generate"),
    path('gapl_generate_irn/<str:inv_no>/', gapl_generate_irn, name="gapl_generate_irn"),
    path('gapl_cancel_irn/<str:irn>/', gapl_cancel_irn, name="gapl_cancel_irn"),
    path('gapl_labour_cancel_irn/<str:irn>/', gapl_labour_cancel_irn, name="gapl_labour_cancel_irn"),
    path('gapl_cancel_irn_form/<str:irn>/', gapl_cancel_irn_form, name="gapl_cancel_irn_form"),
    path('gapl_labour_cancel_irn_form/<str:irn>/', gapl_labour_cancel_irn_form, name="gapl_labour_cancel_irn_form"),

    path('gapl_eway_bill_form/<str:inv_no>/<str:doc_date>/<int:itr_id>/', gapl_eway_bill_form,
         name="gapl_eway_bill_form"),
    path('gapl_labour_eway_bill_form/<str:inv_no>/<str:doc_date>/<int:itr_id>/', gapl_labour_eway_bill_form,
         name="gapl_labour_eway_bill_form"),
    path('gapl_eway_bill_form_admin/<str:inv_no>/<str:doc_date>/<int:itr_id>/', gapl_eway_bill_form_admin,
         name="gapl_eway_bill_form_admin"),
    path('gapl_transport_mode_jquery/', gapl_transport_mode_jquery, name="gapl_transport_mode_jquery"),
    path('gapl_transport_gst_jquery/', gapl_transport_gst_jquery, name="gapl_transport_gst_jquery"),

    # ------------------------ MK Auto -----------------------------------------------

    path('mkauto_iris_form/', mkauto_iris_from, name="mkauto_iris_from"),
    path('mkauto_iris_from_admin_view/', mkauto_iris_from_admin_view, name="mkauto_iris_from_admin_view"),
    path('mkauto_qr_code_generate/<str:inv_no>/', mkauto_qr_code_generate, name="mkauto_qr_code_generate"),
    path('mkauto_generate_irn/<str:inv_no>/', mkauto_generate_irn, name="mkauto_generate_irn"),
    path('mkauto_cancel_irn/<str:irn>/', mkauto_cancel_irn, name="mkauto_cancel_irn"),
    path('mkauto_cancel_irn_form/<str:irn>/', mkauto_cancel_irn_form, name="mkauto_cancel_irn_form"),

    path('mkauto_eway_bill_form/<str:inv_no>/<str:doc_date>/<int:itr_id>/', mkauto_eway_bill_form,
         name="mkauto_eway_bill_form"),
    path('mkauto_eway_bill_form_admin/<str:inv_no>/<str:doc_date>/<int:itr_id>/', mkauto_eway_bill_form_admin,
         name="mkauto_eway_bill_form_admin"),
    path('mkauto_transport_mode_jquery/', mkauto_transport_mode_jquery, name="mkauto_transport_mode_jquery"),
    path('mkauto_transport_gst_jquery/', mkauto_transport_gst_jquery, name="mkauto_transport_gst_jquery"),

    # --------------- Labour Invoice --------------------

    path('labour_invoice_form/', labour_invoice_form, name="labour_invoice_form"),

    path('gapl_labour_iris_from_admin/', gapl_labour_iris_from_admin, name="gapl_labour_iris_from_admin"),
    path('gapl_labour_iris_from/', gapl_labour_iris_from, name="gapl_labour_iris_from"),
    path('gapl_labour_iris_from/', gapl_labour_iris_from, name="gapl_labour_iris_from"),

    # --------------------------- credit Note ---------------------

    path('gapl_credit_note_screen/', gapl_credit_note_screen, name="gapl_credit_note_screen"),
    path('gapl_credit_irn_generate/<str:credit_note_no>/', gapl_credit_irn_generate, name="gapl_credit_irn_generate"),
    path('gapl_credit_cancel/<str:irn>/<str:credit_note_no>/', gapl_credit_cancel, name="gapl_credit_cancel"),

    path('gapl_debit_note_screen/', gapl_debit_note_screen, name="gapl_debit_note_screen"),
    path('gapl_debit_irn_generate/<str:credit_note_no>/', gapl_debit_irn_generate, name="gapl_debit_irn_generate"),
    path('gapl_debit_cancel/<str:irn>/<str:credit_note_no>/', gapl_debit_cancel, name="gapl_debit_cancel"),

    path('gapl_labour_generate_irn/<str:inv_no>/', gapl_labour_generate_irn, name="gapl_labour_generate_irn"),
    # path('gapl_labour_generate_irn_admin/<str:inv_no>/', gapl_labour_generate_irn, name="gapl_labour_generate_irn"),


]
