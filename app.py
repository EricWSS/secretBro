from flask import Flask, request, jsonify
from configs.models import db, User, DatabaseConnection

app = Flask(__name__)

# # Configuração do banco de dados
# app.config["DATABASE_URL"] = "postgresql://user:password@host:port/database_name"

# Inicializar a conexão com o banco
db = DatabaseConnection()

@app.route("/aleluia/add", methods=["POST"])
def add_user():
    try:
        # Verifica se a requisição contém os dados necessários
        data = request.json
        if not data or not data.get("user") or not data.get("key_sorteio"):
            return jsonify({"error": "Missing 'user' or 'key_sorteio' in request"}), 400
        
        # Cria um novo usuário
        new_user = User(user=data["user"], key_sorteio=data["key_sorteio"])
        
        # Insere no banco de dados
        session = db.get_session()
        session.add(new_user)
        session.commit()
        session.close()
        
        return jsonify({"message": "User added successfully", "user": data["user"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/verify-key", methods=["GET"])
def verify_key():
    try:
        # Obtém a chave da URL (parâmetro 'key')
        key = request.args.get("key")
        if not key:
            return jsonify({"error": "Key parameter is required"}), 400
        
        # Conecta ao banco e verifica a correspondência
        session = db.get_session()
        user = session.query(User).filter_by(key_sorteio=key).first()
        session.close()
        
        if user:
            return jsonify({"message": "Key is valid", "user_id": user.id, "user": user.user}), 200
        else:
            return jsonify({"message": "Key is invalid"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
