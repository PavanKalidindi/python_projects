from datetime import datetime
class Email:
    def __init__(self, sender: 'User', receiver: 'User', subject: str, body: str):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = datetime.now()
        self.subject = subject
        self.body = body
        self.read = False

    def __str__(self) -> str:
        status = "Read" if self.read else 'Unread'
        return f"[{status}] From: {self.sender.name} | Subject: {self.subject} | Time: {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def mark_as_read(self):
        """Marks the email as read"""
        self.read = True

    def show_email(self) -> None:
        """shows the full email"""
        self.mark_as_read()
        print("\n--- Email ---")
        print(f"From: {self.sender.name}")
        print(f"To: {self.receiver.name}")
        print(f"Subject: {self.subject}")
        print(f"Received: {self.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print(f"Body: {self.body}")
        print(f"------------\n  ")


class User:
    def __init__(self, name):
        self.name = name
        self.inbox = Inbox()

    def __str__(self):
        return self.name

    def send_email(self, receiver: 'User', subject: str, body: str):
        """Sends the email to receiver"""
        email = Email(sender=self, receiver=receiver, subject=subject, body=body)
        receiver.inbox.receive_email(email)
        print(f"Email sent from {self.name} to {receiver.name}!\n")

    def check_inbox(self) -> None:
        """Shows all emails in inbox"""
        print(f"{self.name}'s Inbox:")
        self.inbox.list_emails()

    def read_email(self, email_number: int):
        """Shows the specified email"""
        self.inbox.read_email(email_number)
        
    def delete_email(self, email_number: int):
            """removes the specified email from inbox"""
            self.inbox.delete_email(email_number)

class Inbox:
    def __init__(self):
        self.emails: list[Email] = []

    def receive_email(self, email: Email) -> None:
        """adds email to inbox"""
        self.emails.append(email)

    def list_emails(self) -> None:
        """Shows all emails from inbox"""
        if not self.emails:
            print("Inbox is empty")
            return
        print("\nYour Emails:")
        for i, email in enumerate(self.emails, start=1):
            print(f"{i}. {email}")

        print("------------\n")

    def read_email(self, email_number: int) -> None:
        """shows the specified email"""
        if not self.emails:
            print("Inbox is empty")
            return
        index = email_number - 1

        if index < 0 or index >= len(self.emails):
            print("Invalid email number.\n")
            return
        
        self.emails[index].show_email()

    def delete_email(self, email_number: int) -> None:
        """Removes the specified email from inbox"""
        if not self.emails:
            print("Inbox is empty")
            return
        index = email_number - 1

        if index < 0 or index >= len(self.emails):
            print("Invalid email number.\n")
            return

        del self.emails[index]
        print("Email deleted.\n")

def main():
    tory = User('Tory')
    ramy = User('Ramy')        
    
    tory.send_email(ramy, 'Hello', 'Hi Ramy, just saying hello!')
    ramy.send_email(tory, 'Re: Hello', 'Hi Tory, hope you are fine.')

    ramy.check_inbox()
    ramy.read_email(1)
    ramy.delete_email(1)
    ramy.check_inbox()
    
    
if __name__ == '__main__':
    main()