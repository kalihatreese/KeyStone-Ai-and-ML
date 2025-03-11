from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Automation & Consulting</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; text-align: center; }
        .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.2); }
        h1 { color: #007BFF; }
        p { font-size: 18px; }
        .cta-button { background-color: #007BFF; color: white; padding: 15px 20px; text-decoration: none; font-size: 20px; border-radius: 5px; display: inline-block; margin-top: 20px; }
        .cta-button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AI Automation & Consulting</h1>
        <p>We help businesses automate workflows, save time, and increase revenue using AI-powered solutions.</p>
        <ul style="text-align: left; padding-left: 30px;">
            <li>✔ AI Chatbots & Customer Support Automation</li>
            <li>✔ AI Sales & Lead Generation Systems</li>
            <li>✔ AI-Driven Marketing & Predictive Analytics</li>
        </ul>
        <p><strong>🎯 Book a Free AI Strategy Call</strong></p>
        <a href="https://calendly.com/YOUR-CALENDLY-LINK" class="cta-button">📅 Book a Free Call</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
