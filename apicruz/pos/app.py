from app import create_app

app = create_app()
    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify({"mensagem": "Olá, mundo!"})

    @app.route("/mensagens", methods=["GET"])
    def listar_mensagens():
        return jsonify({
            "mensagens": [
                "Primeira mensagem",
                "Segunda mensagem"
            ]
        })

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)