from flask import Flask

def hello_world():
    return '<p>Hello, World!</p>\n'

header_text = """
    <html>\n<head><title>Congressional Stock Trading Monitor</title></head>\n<body>"""
footer_text = """
    </body>\n</html>"""

application = Flask(__name__)

application.add_url_rule('/', 'index', (lambda: header_text + hello_world() + footer_text))

if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", port=5000)
    
