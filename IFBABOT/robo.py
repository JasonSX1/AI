from chatterbot import ChatBot

NOME_ROBO = "IFBABot"
CONFIANCA_MINIMA = 0.60

def configurar_robo():

    robo = ChatBot(NOME_ROBO, read_only = True)
    return robo

def executar_robo(robo):
    print("🤖 IFBABot iniciado! (Digite 'sair' para encerrar)\n")
    while True:
        mensagem = input("👤 Você: ")
        if mensagem.lower() in ["sair", "tchau", "exit"]:
            print("👾 IFBABot: Até mais!")
            break
        resposta = robo.get_response(mensagem.lower())
        if resposta.confidence >= CONFIANCA_MINIMA:
            print(f"👾 IFBABot: {resposta} [confiança = {resposta.confidence}]")
        else:
            print(f"👾 Ainda não sei responder essa pergunta. Pergunte outra coisa!  [confiança = {resposta.confidence}]")

if __name__ == "__main__":
    robo = configurar_robo()
    executar_robo(robo)
