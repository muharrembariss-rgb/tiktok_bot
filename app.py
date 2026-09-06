from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8951301678:AAEaVloU4VLoAOXy7a-mhdMmA-SGXsQOWBY"
TELEGRAM_CHAT_ID = "7647963196"

def telegrama_bildirim_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram Yaniti:", response.status_code, response.text)
    except Exception as e:
        print("Telegram hatasi:", e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sonucu-kaydet', methods=['POST'])
def sonucu_kaydet():
    veri = request.json
    puan = veri.get('puan')
    cevaplar = veri.get('cevaplar', [])
    
    mesaj = f"🚨 <b>Arifenur Testi Tamamladi!</b> ❤️\n\n" \
            f"🏆 <b>Toplam Puan:</b> {puan} / 7\n\n" \
            f"📝 <b>Verdigi Cevaplar:</b>\n"
    
    for idx, cevap in enumerate(cevaplar, 1):
        durum = "✅ Dogru" if cevap.get('dogruMu') else "❌ Yanlis"
        mesaj += f"Soru {idx}: {cevap.get('secim')} ({durum})\n"
        
    telegrama_bildirim_gonder(mesaj)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)