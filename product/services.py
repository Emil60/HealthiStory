from django.core.mail import send_mail
from django.conf import settings


def mobile_station_order_send_mail(**kwargs):
    """Send mail to user with order information"""
    email_from = settings.EMAIL_HOST_USER
    subject = "New Order"
    message = f"""
        Customer Information:
            Email:                  {kwargs['email']}
            Name and Surname:       {kwargs['name']}
            Phone:                  {kwargs['phone']}
            Delivery address:       {kwargs['address']}

        Quantity of products:
            Number of required Mobile Medi-Lab:                                 {kwargs['station_amount']}
            Number of required Checkup Capacity:                                {kwargs['capacity_number']}
            Number of required RFID Card:                                       {kwargs['card_number']}
            Number of required Lancet:                                          {kwargs['lancet_number']}
            Number of required Glucose/Hematocrit strip:                        {kwargs['glucose_number']}
            Number of required Ketone strip:                                    {kwargs['ketone_number']}
            Number of required Lipid Panel (TC + HDL + Triglyceride) + pipet:   {kwargs['panel_number']}
            Number of required Total Cholesterol (TC) + HDL strip + pipet:      {kwargs['cholesterol_number']}
            Number of required Uric Acid strip:                                 {kwargs['acid_number']}
            Number of required Creatinine strip:                                {kwargs['creatinine_number']}"""

    if kwargs['station_amount'] or kwargs['capacity_number'] or kwargs['card_number'] or kwargs['lancet_number'] or kwargs['glucose_number'] or kwargs['ketone_number'] or kwargs['panel_number'] or kwargs['cholesterol_number'] or kwargs['acid_number'] or kwargs['creatinine_number']:
        recipient_list = ['shahlar.pashayev@myhealthistory.com']
        send_mail(subject, message, email_from, recipient_list)
        return 1
    else:
        return 0


def symptom_check_order_send_mail(**kwargs):
    """Send mail to user with order information"""
    email_from = settings.EMAIL_HOST_USER
    subject = "New order"
    message = f"""
        Customer Information:
            Email:                  {kwargs['email']}
            Name and Surname:       {kwargs['name']}
            Phone:                  {kwargs['phone']}
            Delivery address:       {kwargs['address']}

        Quantity of products:
            Number of required Symptom Check set:      {kwargs['symptom_check_set_amount']}"""
    recipient_list = ['shahlar.pashayev@myhealthistory.com']
    send_mail(subject, message, email_from, recipient_list)
    return 1
