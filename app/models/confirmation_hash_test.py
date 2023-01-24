import smtplib
import hashlib
import pdb
from email.mime.text import MIMEText
import webbrowser



def generate_confirmation_hash(email):
    email = email.encode()
    hash_object = hashlib.sha256()
    hash_object.update(email)
    hex_dig = hash_object.hexdigest()
    conf_string = str(hex_dig)
    conf_hash = ''
    for letter in conf_string[:6]:
        if type(letter) == int:
            conf_hash+=str(letter)
        elif type(letter) == str:
            conf_hash+=letter.upper()
        else:
            pass
    return conf_hash

def send_confirmation_email(email, confirmation_hash):
    msg = MIMEText("Your confirmation code is: " + confirmation_hash)
    msg['Subject'] = 'Email Confirmation'
    msg['From'] = 'EMAIL@EMAIL.com' #PONER EMAIL Y APP PASSWORD
    msg['To'] = email

    # Connect to the email server using SSL
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to the email server
    server.login("EMAIL@EMAIL.com", "APPPASWORD") #PONER EMAIL Y APP PASSWORD

    # Send the email
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    # Close the connection to the email server
    server.quit()


