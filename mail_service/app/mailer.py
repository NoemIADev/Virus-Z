


from azure.communication.email import EmailClient
import traceback
import os
connection_string = os.getenv("AZURE_EMAIL_CONNECTION_STRING")

client = EmailClient.from_connection_string(connection_string)

def send_mail(messageAlerte, emails):
    try:
        message = {
            "senderAddress": "DoNotReply@9eb8b9a9-fe7f-4e4f-8aa8-feca29eaace0.azurecomm.net",
            "recipients": {
                "to": [{"address": email} for email in emails]
            },
            "content": {
                "subject": "Alerte contagion",
                "plainText": messageAlerte,
            },
        }

        poller = client.begin_send(message)
        result = poller.result()
        print("Status:", result["status"])

    except Exception:
        traceback.print_exc()

print(os.getenv("AZURE_EMAIL_CONNECTION_STRING"))