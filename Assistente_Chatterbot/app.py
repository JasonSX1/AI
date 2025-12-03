from flask import Flask, render_template, request, jsonify
try:
    from bot import configurar_robo
except Exception as e:
    print(f"⚠️  Erro ao importar bot real: {e}")
    from mock_bot import configurar_robo

app = Flask(__name__)
robo = configurar_robo()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data.get("msg")
    
    if not user_input:
        return jsonify({"response": "Mensagem vazia."}), 400

    try:
        response = robo.get_response(user_input)
        return jsonify({
            "response": str(response),
            "confidence": float(response.confidence)
        })
    except Exception as e:
        return jsonify({"response": f"Erro: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
