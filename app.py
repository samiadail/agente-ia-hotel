#Importando as bibliotecas
from flask import Flask,jsonify,request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv
from supabase import create_client
import os

#Leitura da chave de API
load_dotenv()
#Usando o getenv para pegar o arquivo específico
supabase_url = os.getenv("SUPABASE_URL")
#Usando o getenv para pegar o arquivo específico
supabase_key = os.getenv("SUPABASE_KEY")
#Criando a conexão com o banco de dados, passando a URL e a KEY.
supabase = create_client(supabase_url,supabase_key)


#Criar o nosso app
app = Flask (__name__)
#Habilitar o cors
CORS(app)

#Criar o agente
agente = Agent (
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é um agente virtual do Hotel Travesseiro Nervoso, slogan: Aqui até a insônia dorme"
    "Você responde de forma clara e humorada, informações sobre quartos,serviços, reservas e preços"
    "Quarto Standard ($500), Quarto Deluxe ($700), Quarto Suíte Presidencial ($1000)"
    "Serviços oferecidos: Academia, Café da Manhã, Lavanderia, Restaurante, Piscina"
    "Não inclua icones em markdown nas respostas, como: ##, **",
   
    markdown=True
)

#Criar a rota VAZIA e o método GET
@app.route("/", methods=['GET'])
def testar():
    return jsonify({"mensagem":"API funcionando"})

#Criar a rota e o método POST
@app.route("/chat",methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados['pergunta']
    resposta = agente.run(pergunta)
    return jsonify({"resposta":resposta.content})


#Criar a rota para servas
@app.route("/reservar", methods=['POST'])
def reservar():
    dados = request.get_json()
    nova_reserva = {
        "nome":dados["nome"],
        "email":dados["email"],
        "check_in":dados["check_in"],
        "tipo_quarto":dados["tipo_quarto"]
    }
    supabase.table("reservas").insert(nova_reserva).execute()
    return jsonify({"mensagem":"Reserva realizada com sucesso!"})


#Rodar o nosso app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)