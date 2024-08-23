from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail
import os

def send_email(subject, recipient, body):
    SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')

    configuration = Configuration()
    configuration.api_key['api-key'] = SENDINBLUE_API_KEY

    api_client = ApiClient(configuration)
    email_api = TransactionalEmailsApi(api_client)

    send_smtp_email = SendSmtpEmail(
        to=[{'email': recipient}],
        sender={'email': 'barralfranco740@gmail.com'},
        subject=subject,
        text_content=body
    )

    try:
        response = email_api.send_transac_email(send_smtp_email)
        print("Email sent successfully.")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
