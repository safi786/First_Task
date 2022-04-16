import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename


def send_email(reciever):
    password = 'password'
    # port = 465  # For SSL
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "test@gmail.com"  # Enter your address

    messagefile = open("email_content.txt")
    body = """\
    """ + messagefile.read()
    messagefile.close()

    # context = ssl.create_default_context()
    # with smtplib.SMTP(smtp_server, port) as server:
    #     server.ehlo()  # Can be omitted
    #     server.starttls(context=context)
    #     server.ehlo()  # Can be omitted
    #     try:
    #         print(server.login(sender_email, password))
    #     except:
    #         print(server.login(sender_email, password))
    #         print("Error! Connection Failed. Please check account credentials")
    #     for receiver in receivers:
    #         try:
    #             print(server.sendmail(sender_email, receiver, message))
    #             print("Email successfully sent to : ", receiver)
    #         except:
    #             print("Sending email operation failed for : ", receiver)
    #


    message = MIMEMultipart("alternative")
    message["Subject"] = os.environ.get('subject')
    message["From"] = sender_email
    message["To"] = reciever


    part2 = MIMEText(body, "html")

    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

        try:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, reciever, message.as_string()
            )
            print("Email successfully sent to ", reciever)
            server.close()
        except Exception as e:
            print(e)