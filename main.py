import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
from colorama import Fore, Style, init
import time
import os
import shutil

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center(text, width=None):
    if width is None:
        width = shutil.get_terminal_size().columns
    return text.center(width)

def show_logo():
    logo = f"""
{Fore.CYAN}{Style.BRIGHT}
  ___ __  __   _   ___ _      _____ ___   ___  _    
 | __|  \/  | /_\ |_ _| |    |_   _/ _ \ / _ \| |   
 | _|| |\/| |/ _ \ | || |__    | || (_) | (_) | |__ 
 |___|_|  |_/_/ \_\___|____|   |_| \___/ \___/|____|
{Fore.YELLOW}
            Gmail Broadcaster by N4S | Safe Edition
{Style.RESET_ALL}
"""
    for line in logo.splitlines():
        print(center(line))

def prompt_input(label):
    return input(Fore.GREEN + center("👉 " + label + ": "))

def load_recipients(file='email.txt'):
    if not os.path.exists(file):
        print(Fore.RED + center(f"❌ File '{file}' not found.\n"))
        return []
    with open(file, 'r') as f:
        emails = [line.strip() for line in f if line.strip()]
    if not emails:
        print(Fore.RED + center("❌ The 'email.txt' file is empty.\n"))
    return emails

def send_emails(sender, password, subject, body, recipients):
    print(Fore.YELLOW + "\n" + center("📡 Connecting to Gmail...\n"))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        print(Fore.GREEN + center("✅ Login successful.\n"))
        for recipient in recipients:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(sender, recipient, msg.as_string())
            print(Fore.BLUE + center(f"📨 Email sent to {recipient}"))
            time.sleep(0.5)
        server.quit()
        print(Fore.GREEN + "\n" + center("🎉 All emails were sent successfully.\n"))
    except smtplib.SMTPAuthenticationError:
        print(Fore.RED + center("❌ Authentication error. Use an app password.\n"))
    except Exception as e:
        print(Fore.RED + center(f"❌ An error occurred: {e}\n"))

def main():
    clear_screen()
    show_logo()
    sender = prompt_input("Enter your Gmail address")
    password = getpass.getpass(Fore.GREEN + center("🔐 Enter your Gmail password (or app password): "))
    subject = prompt_input("Enter the email subject")
    body = prompt_input("Enter the email message")
    recipients = load_recipients()
    if recipients:
        send_emails(sender, password, subject, body, recipients)

if __name__ == "__main__":
    main()
