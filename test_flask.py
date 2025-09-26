# Basit Flask testi
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "✅ Flask çalışıyor! FHE Sanat projesi hazır."

if __name__ == '__main__':
    print("🧪 Flask test başlatılıyor...")
    app.run(debug=True, port=5001)
    