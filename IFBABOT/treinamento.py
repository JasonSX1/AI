from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

# Caminhos dos arquivos de conversas
CONVERSAS = [
    "C:\\Users\\Aluno\\Desktop\\IFBABOT\\conversas\\saudacoes.json",
    "C:\\Users\\Aluno\\Desktop\\IFBABOT\\conversas\\informacoes_basicas.json",
    "C:\\Users\\Aluno\\Desktop\\IFBABOT\\conversas\\sistemas_de_informacao.json"
]

NOME_ROBO = "IFBABot"

def configurar_treinador():
    """Cria o chatbot e o treinador"""
    robo = ChatBot(NOME_ROBO)
    treinador = ListTrainer(robo)
    return treinador

def carregar_conversas():
    """Carrega as conversas a partir dos arquivos JSON"""
    conversas = []
    for arquivo_conversas in CONVERSAS:
        with open(arquivo_conversas, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            conversas.append(dados["conversas"])
    return conversas

def treinar(treinador, conversas):
    """Treina o chatbot com as mensagens e respostas"""
    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]

            for mensagem in mensagens:
                print(f"Treinando mensagem: '{mensagem}' -> '{resposta}'")
                treinador.train([mensagem.lower(), resposta])

if __name__ == "__main__":
    treinador = configurar_treinador()
    conversas = carregar_conversas()

    if treinador and conversas:
        treinar(treinador, conversas)
        print("\n✅ Treinamento concluído com sucesso!")
    else:
        print("\n⚠️ Nenhuma conversa encontrada para treinar.")
