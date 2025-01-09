import uuid

from django.db import models


# Create your models here.


class EmpanelledIrps(models.Model):
    psk_uid = models.UUIDField(default=uuid.uuid4, editable=False)
    irp_name = models.CharField(max_length=200)
    url_type = models.CharField(max_length=200)
    url_link = models.CharField(max_length=350, unique=True)

    class Meta:
        db_table = 'gst_empanelled_irps '

    def __str__(self):
        return self.irp_name


class Company(models.Model):
    irp_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    company_id = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    user_gstin = models.CharField(max_length=200)
    api_url = models.CharField(max_length=350)
    api_type = models.CharField(max_length=200)
    token = models.CharField(max_length=1000)
    api_response = models.TextField()

    class Meta:
        db_table = 'gst_company'

    def __str__(self):
        return self.company_name


class GstIrnEwayBillLog(models.Model):
    api_einvoice_no = models.CharField(max_length=10000, null=True)
    api_einvoice_date = models.CharField(max_length=10000, null=True)
    api_ewaybill_no = models.CharField(max_length=10000, null=True)
    api_ewaybill_date = models.CharField(max_length=10000, null=True)
    api_ewaybill_validtill = models.CharField(max_length=10000, null=True)
    api_status_message = models.CharField(max_length=10000, null=True)
    qrcode = models.TextField(null=True)
    no = models.CharField(max_length=10000, null=True)
    gen_by = models.CharField(max_length=10000, null=True)
    gen_by_name = models.CharField(max_length=10000, null=True)
    add_to_db = models.BooleanField(null=True)
    dup_irn = models.BooleanField(null=True)
    status = models.CharField(max_length=10000, null=True)
    ack_no = models.BigIntegerField(null=True)
    ack_dt = models.CharField(max_length=10000, null=True)
    irn = models.CharField(max_length=10000, null=True)
    signed_qr_code = models.CharField(max_length=10000, null=True)
    api_response = models.TextField(null=True)
    api_payload = models.TextField(null=True)
    api_payload_ewaybill = models.TextField(null=True)
    api_response_ewaybill = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.TextField(null=True)
    irn_status = models.CharField(max_length=10000, null=True)
    # itr_id = models.CharField(max_length=200, null=True)
    # qr_code_url = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'gst_irn_ewaybill_log'

    def __str__(self):
        return self.api_einvoice_no
