import os
from agentmail import AgentMail

class EmailService:
    def __init__(self, config_data: dict, settings: dict, html_payload: str):
        self.config_data = config_data
        self.settings = settings
        self.html_payload = html_payload

    def send_email(self) -> bool:
        api_key = self.config_data.get('agentmail_api_key', '')
        inbox_id = self.config_data.get('agentmail_inbox_id', '')
        email_subject = self.config_data.get('email_subject', 'AFS Test')
        
        if not api_key or not inbox_id:
            print("Error: Missing AgentMail API Key or Inbox ID. Check your settings.")
            return False

        try:
            client = AgentMail(api_key=api_key)
            
            if self.config_data.get('sendAfsDirect') in ['off', None, False, '']:
                recipient = self.settings.get('recipientEmail', {}).get('value', '')
                bcc = self.config_data.get('afs_email', '')
            else:
                recipient = self.config_data.get('afs_email', '')
                bcc = None

            print(f"Sending via AgentMail to {recipient} / bcc {bcc} through inbox {inbox_id}...")
            
            client.inboxes.messages.send(
                inbox_id=inbox_id,
                to=recipient,
                subject=email_subject,
                text=self.html_payload,
                html=self.html_payload,
                bcc=bcc if bcc else None
            )
            
            print("Email sent successfully via AgentMail API.")
            return True
        except Exception as e:
            print(f"Failed to send email via AgentMail: {e}")
            return False
