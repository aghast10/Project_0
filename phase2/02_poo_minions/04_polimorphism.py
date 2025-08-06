'''Task: Notification System
Base class: Notification with method send().
Subclasses: Email, SMS, PushNotification, each with a different send() implementation.
Create a function that iterates through a list of notifications and sends them.'''

class Notification:
    def send(self):
        print("hola") 
class Email(Notification):
    def send(self):
        print ("you have unread emails")
class Sms(Notification):
    def send(self):
        print ("you received a new sms")
class PushNotification(Notification):
    def send(self):
         print("Push notification incoming")
         
for notification in [Email(), Sms(), PushNotification()]:
    notification.send()