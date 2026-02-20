
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from data_base import conectar_banco 


app = Flask(__name__)
CORS(app)

@app.route('/auth', methods=['POST'])
def autenticacao():
    db = conectar_banco()

    if db is None:
        return jsonify({"success": False, "message": "Erro conexão banco"}), 500

    cursor = db.cursor(dictionary=True)
    dados = request.get_json()

    if not dados:
        return jsonify({"success": False, "message": "Dados inválidos"}), 400

    email = dados.get("email")
    senha = dados.get("senha")
    acao = dados.get("acao")


# ---------------- LOGIN ---------------- #
    if acao == "login":

        # Busca usuário apenas pelo email
        cursor.execute(
            "SELECT * FROM usuario WHERE email=%s",
            (email,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        db.close()

        # Verifica se usuário existe
        if not usuario:
            return jsonify({
                "success": False,
                "message": "Usuário não encontrado"
            }), 401

        # Verifica senha
        if usuario["senha"] != senha:
            return jsonify({
                "success": False,
                "message": "Senha incorreta"
            }), 401

        # Se chegou aqui, login é válido
        return jsonify({
            "success": True,
            "message": "Login autorizado",
            "usuario_id": usuario["id_usuario"]
        })


    # ---------------- CADASTRO ---------------- #
    elif acao == "cadastrar":

        nome_user = dados.get("nome_user")
        cpf = dados.get("cpf")
        data_nascimento = dados.get("data_nascimento")
        peso = dados.get("peso")
        altura = dados.get("altura")
        cep = dados.get("cep")
        cidade_user = dados.get("cidade_user")
        uf_user = dados.get("uf_user")

        try:
            print(dados)

            cursor.execute("""
                INSERT INTO usuario 
                (nome_user, cpf, data_nascimento, peso, altura, email, senha, cep, cidade_user, uf_user)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nome_user,
                cpf,
                data_nascimento,
                peso,
                altura,
                email,
                senha,
                cep,
                cidade_user,
                uf_user
            ))

            db.commit()

        except mysql.connector.Error as erro:
            print("Erro ao cadastrar:", erro)

            if erro.errno == 1062:
                return jsonify({
                    "success": False,
                    "message": "Este CPF ou email já está cadastrado."
                }), 400

            return jsonify({
                "success": False,
                "message": "Erro ao cadastrar usuário."
            }), 400


        finally:
            cursor.close()
            db.close()

        return jsonify({"success": True})

    cursor.close()
    db.close()
    return jsonify({"success": False}), 400


# ---------------- EVENTOS ---------------- #

@app.route('/eventos', methods=['GET'])
def listar_eventos():
    db = conectar_banco()

    if db is None:
        return jsonify({"erro": "Erro conexão banco"}), 500

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM eventos")
    eventos = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(eventos)


@app.route('/eventos', methods=['POST'])
@app.route('/eventos', methods=['POST'])
def criar_evento():
    db = conectar_banco()

    if db is None:
        return jsonify({"success": False, "message": "Erro conexão banco"}), 500

    dados = request.get_json()

    if not dados:
        return jsonify({"success": False, "message": "Dados inválidos"}), 400

    try:
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO evento (
                nome_evento,
                tipo,
                faixa_etaria,
                genero,
                esporte_evento,
                descricao_evento,
                horario_inicio,
                horario_termino,
                max_jogadores,
                qtd_times,
                jogadores_time,
                valor_aluguel,
                horas_aluguel,
                pix,
                beneficiario,
                banco,
                rua_numero,
                cidade_evento,
                bairro_evento,
                cep_evento,
                ponto_ref,
                codigo_convite,
                usuario_id,
                quadra_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            dados.get("nome_evento"),
            dados.get("tipo"),
            dados.get("faixa_etaria"),
            dados.get("genero"),
            dados.get("esporte_evento"),
            dados.get("descricao_evento"),
            dados.get("horario_inicio"),
            dados.get("horario_termino"),
            dados.get("max_jogadores"),
            dados.get("qtd_times"),
            dados.get("jogadores_time"),
            dados.get("valor_aluguel"),
            dados.get("horas_aluguel"),
            dados.get("pix"),
            dados.get("beneficiario"),
            dados.get("banco"),
            dados.get("rua_numero"),
            dados.get("cidade_evento"),
            dados.get("bairro_evento"),
            dados.get("cep_evento"),
            dados.get("ponto_ref"),
            dados.get("codigo_convite"),
            dados.get("usuario_id"),
            dados.get("quadra_id")
        ))

        db.commit()
        evento_id = cursor.lastrowid

    except mysql.connector.Error as erro:
        print("Erro ao criar evento:", erro)
        return jsonify({
            "success": False,
            "message": str(erro)
        }), 400

    finally:
        cursor.close()
        db.close()

    return jsonify({
        "success": True,
        "message": "Evento criado com sucesso",
        "evento_id": evento_id
    }), 201

# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
