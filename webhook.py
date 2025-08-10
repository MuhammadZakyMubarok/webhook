from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ==== Konfigurasi Telegram ====
TELEGRAM_BOT_TOKEN = "7709470943:AAG4f1-HT4q_YS8Z7BfVwLC8doN54erewPk"
TELEGRAM_CHAT_ID = "6154989723"  # ID pribadi atau grup
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        # Pastikan data dari MQL5 sesuai format
        symbol = data.get("symbol", "UNKNOWN")
        signal = data.get("signal", "UNKNOWN")
        price = data.get("price", 0)
        rsi = data.get("rsi", 0)
        ema5 = data.get("ema5", 0)
        ema20 = data.get("ema20", 0)
        ema200 = data.get("ema200", 0)
        atr = data.get("atr", 0)

        # Format pesan Telegram
        message = (
            f"📢 *Trading Signal Received*\n"
            f"Symbol: `{symbol}`\n"
            f"Signal: *{signal}*\n"
            f"Price: `{price}`\n"
            f"RSI: `{rsi}`\n"
            f"EMA5: `{ema5}`\n"
            f"EMA20: `{ema20}`\n"
            f"EMA200: `{ema200}`\n"
            f"ATR: `{atr}`"
        )

        # Kirim ke Telegram
        requests.post(TELEGRAM_URL, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })

        return jsonify({"status": "success", "message": "Signal received"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
