import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
from colorama import Fore, Style, init
import time
import os

init(autoreset=True)

def show_logo():
    logo = f"""
{Fore.CYAN}{Style.BRIGHT}
  ___ __  __   _   ___ _      _____ ___   ___  _    
 | __|  \/  | /_\ |_ _| |    |_   _/ _ \ / _ \| |   
 | _|| |\/| |/ _ \ | || |__    | || (_) | (_) | |__ 
 |___|_|  |_/_/ \_\___|____|   |_| \___/ \___/|____|
                                                    
{Fore.YELLOW}        Email Spam By N4S | Gmail to Gmail
{Style.RESET_ALL}
"""
    print(logo)

def prompt_input(text):
    return input(Fore.GREEN + "👉 " + text + ": ")

def load_recipients(file='email.txt'):
    if not os.path.exists(file):
        print(Fore.RED + f"❌ File '{file}' not found.")
        return []
    with open(file, 'r') as f:
        emails = [line.strip() for line in f if line.strip()]
    if not emails:
        print(Fore.RED + "❌ The 'email.txt' file is empty.")
    return emails

def send_emails(sender, password, subject, body, recipients):
    print(Fore.YELLOW + "\n📡 Connecting to Gmail...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        print(Fore.GREEN + "✅ Login successful.\n")
        for recipient in recipients:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(sender, recipient, msg.as_string())
            print(Fore.BLUE + f"📨 Email sent to {recipient}")
            time.sleep(0.5)
        server.quit()
        print(Fore.GREEN + "\n🎉 All emails were sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print(Fore.RED + "❌ Authentication error. Use an app password.")
    except Exception as e:
        print(Fore.RED + f"❌ An error occurred: {e}")

def main():
    show_logo()
    sender = prompt_input("Enter your Gmail address")
    password = getpass.getpass(Fore.GREEN + "🔐 Enter your Gmail password (or app password): ")
    subject = prompt_input("Enter the email subject")
    body = prompt_input("Enter the email message")
    recipients = load_recipients()
    if recipients:
        send_emails(sender, password, subject, body, recipients)

if __name__ == "__main__":
    main()
