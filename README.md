# 🎣 AI-Powered Spear Phishing Simulator

> A Python-based social engineering tool that leverages Google Gemini AI (LLM) to generate highly convincing, context-aware spear-phishing emails for security awareness training.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=flat&logo=google)
![Security](https://img.shields.io/badge/Type-Social%20Engineering-red)

## 🧐 The Project
Modern phishing attacks are no longer full of typos; they are targeted and personalized. This tool demonstrates how **Generative AI** can be used to automate **Spear Phishing** campaigns.

It takes a target's details (Name, Scenario, Sender Alias) and uses **Google Gemini** to craft a realistic, persuasive email. It then wraps the content in a **Fake Gmail UI** for previewing before delivering the payload via SMTP.

## ✨ Features
* **🤖 Generative AI Engine:** Uses `google.generativeai` to dynamically write email bodies based on custom scenarios (e.g., "Netflix Payment Failed" or "Urgent HR Update").
* **📧 Automated Delivery:** Integrates with Python's `smtplib` for instant delivery.
* **👁️ Visual Preview:** Automatically generates and opens a `preview.html` file that mimics the Gmail interface, allowing the attacker to verify the "look and feel" before sending.
* **🎯 Spear Phishing Mode:** Injects specific target names and sender aliases to increase credibility.

## ⚠️ Legal Disclaimer
**FOR EDUCATIONAL PURPOSES ONLY.**
This software is developed for **Authorized Security Testing** and **Educational Use**. Do not use this tool against targets without prior mutual consent. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

## 🚀 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Ajajay44/PHISHSIM-phishing-email-generator.git
    cd PHISHSIM-phishing-email-generator
    ```

2.  **Install Dependencies**
    ```bash
    pip install google-generativeai
    ```

3.  **Configuration**
    Open `phishsim.py` and update the following:
    * `SENDER_EMAIL`: Your Sender Gmail address.
    * `SENDER_PASSWORD`: Your Google App Password (not login password).
    * `GEMINI_API_KEY`: Your API key from Google AI Studio.

## 💻 Usage

Run the script in your terminal:

```bash
python phishsim.py
```
Demo Screenshots:

![Demo Screenshots](<demo2.png>)



![Demo Screenshots](<demo1.png>)
