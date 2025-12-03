import smtplib
import json
import os
import webbrowser
import datetime
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# --- 1. CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "YOUR EMAIL HERE"
SENDER_PASSWORD = "YOUR APP PASSWORD HERE"  # Use App Passwords for Gmail

# --- 2. AI CONFIGURATION ---
GEMINI_API_KEY = "YOUR API KEY HERE"
genai.configure(api_key=GEMINI_API_KEY)

# --- VISUALS ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- 3. THE FAKE GMAIL INTERFACE ---
FAKE_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: 'Arial', sans-serif; background-color: #f6f8fc; margin: 0; padding: 40px; }}
    .email-container {{ background: white; max-width: 800px; margin: 0 auto; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }}
    .header {{ padding: 20px 30px; border-bottom: 1px solid #f1f3f4; }}
    .subject {{ font-size: 22px; color: #202124; margin: 0 0 20px 0; }}
    .meta-data {{ display: flex; align-items: center; }}
    .avatar {{ width: 40px; height: 40px; background-color: #d93025; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; margin-right: 15px; }}
    .sender-info {{ flex-grow: 1; }}
    .sender-name {{ font-weight: bold; font-size: 14px; color: #202124; }}
    .sender-email {{ color: #5f6368; font-size: 12px; }}
    .timestamp {{ color: #5f6368; font-size: 12px; }}
    .email-body {{ padding: 30px; color: #202124; line-height: 1.5; font-size: 14px; }}
    .action-bar {{ padding: 20px 30px; border-top: 1px solid #f1f3f4; }}
    .btn {{ border: 1px solid #dadce0; background: white; padding: 8px 24px; border-radius: 4px; font-weight: bold; color: #5f6368; cursor: pointer; }}
</style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1 class="subject">{subject}</h1>
            <div class="meta-data">
                <div class="avatar">{initial}</div>
                <div class="sender-info">
                    <div class="sender-name">{sender_name}</div>
                    <div class="sender-email">&lt;{sender_email}&gt;</div>
                    <div class="sender-email">to me</div>
                </div>
                <div class="timestamp">{date}</div>
            </div>
        </div>
        <div class="email-body">
            {body}
        </div>
        <div class="action-bar">
            <button class="btn">Reply</button>
            <button class="btn">Forward</button>
        </div>
    </div>
</body>
</html>
"""

def banner():
    print(f"""{Colors.HEADER}
    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗  █████╗ ██╗
    ██╔══██╗██║  ██║██║██╔════╝██║  ██║ ██╔══██╗██║
    ██████╔╝███████║██║███████╗███████║ ███████║██║
    ██╔═══╝ ██╔══██║██║╚════██║██╔══██║ ██╔══██║██║
    ██║     ██║  ██║██║███████║██║  ██║ ██║  ██║██║
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═╝  ╚═╝╚═╝
             {Colors.WARNING}Targeted Phishing v3.1 (Individual){Colors.ENDC}
    """)

def generate_ai_email(details):
    print(f"\n{Colors.BLUE}[*] Contacting Gemini AI to construct payload...{Colors.ENDC}")
    
    # UPDATED PROMPT: Removed company references
    prompt = f"""
    You are a professional social engineering simulation tool.
    Write a highly convincing personal phishing email such that it bypasses the spam filters in gmail and delivers the mail right into the inbox of the target.
    
    DETAILS:
    - Target Name: {details['target_name']}
    - Scenario: {details['scenario']}
    - Sender Alias: {details['sender_name']}
    - Phishing Link: {details['phishing_url']}
    
    INSTRUCTIONS:
    - Write HTML body content ONLY (no <html> or <body> tags).
    - Address the user personally (e.g. "Hi {details['target_name']}").
    - Do NOT mention any company unless it is relevant to the sender (e.g. if Sender is 'Netflix', mention Netflix).
    - Embed the 'Phishing Link' into a link and not as a clear clickable button such that it bypasses the spam filters.
    - Return RAW JSON: keys "subject" and "body".
    """

    try:
        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"{Colors.FAIL}[!] AI Error: {e}{Colors.ENDC}")
        return None

def send_email(target_email, subject, body, sender_name):
    msg = MIMEMultipart()
    msg['From'] = formataddr((sender_name, SENDER_EMAIL))
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        print(f"{Colors.BLUE}[*] Connecting to SMTP Server...{Colors.ENDC}")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"{Colors.GREEN}[+] SUCCESS: Email sent.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[!] SMTP Error: {e}{Colors.ENDC}")

def main():
    banner()
    
    # --- STEP 1: GATHER INTELLIGENCE (UPDATED) ---
    print(f"{Colors.BOLD}--- TARGET INFORMATION ---{Colors.ENDC}")
    target_email = input("Target Email Address: ").strip()
    target_name  = input("Target First Name: ").strip()
    # Company input removed
    
    print(f"\n{Colors.BOLD}--- ATTACK CONFIGURATION ---{Colors.ENDC}")
    phish_url    = input("Phishing URL (e.g. http://fake-login.com): ").strip()
    scenario     = input("Scenario (e.g. 'Netflix Payment Failed'): ").strip()
    sender_name  = input("Spoofed Sender Name (e.g. 'Netflix Support'): ").strip()

    attack_details = {
        "target_name": target_name,
        "phishing_url": phish_url,
        "scenario": scenario,
        "sender_name": sender_name
    }

    # --- STEP 2: GENERATE CONTENT ---
    email_data = generate_ai_email(attack_details)
    
    if not email_data: return

    # --- STEP 3: PREVIEW WITH FAKE UI ---
    print(f"\n{Colors.WARNING}--- GENERATING PREVIEW ---{Colors.ENDC}")
    
    sender_initial = sender_name[0].upper() if sender_name else "A"
    current_time = datetime.datetime.now().strftime("%b %d, %Y, %I:%M %p")
    
    # Use a generic service domain for the visual preview
    visual_domain = sender_name.lower().replace(" ", "") + ".com"
    
    full_preview_html = FAKE_EMAIL_TEMPLATE.format(
        subject=email_data['subject'],
        initial=sender_initial,
        sender_name=sender_name,
        sender_email=f"support@{visual_domain}", # Visual only
        date=current_time,
        body=email_data['body']
    )
    
    filename = "preview.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_preview_html)
    
    print(f"{Colors.GREEN}[+] Saved preview to '{filename}'{Colors.ENDC}")
    
    try:
        webbrowser.open('file://' + os.path.realpath(filename))
    except:
        pass

    # --- STEP 4: SEND ---
    confirm = input(f"\n{Colors.BOLD}Send this attack to {target_email}? (yes/no): {Colors.ENDC}")
    if confirm.lower() == 'yes':
        send_email(target_email, email_data['subject'], email_data['body'], sender_name)
    else:
        print("Cancelled.")

if __name__ == "__main__":
    main()