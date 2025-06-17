from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Hello from Flask on Vercel!'})

@app.route('/send-reset-code', methods=['POST'])
def send_code():
    return jsonify({'message': 'Simulated reset code sent'})

if __name__ == "__main__":
    app.run()