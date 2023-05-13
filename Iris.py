import pyttsx3
import speech_recognition as sr
from comandos import ouvir, falar, relogio, pesquisar, abrir, formata_comando  # previsao_tempo

# precisamos sempre do RECOGNIZER e do MICROPHONE para fazer um reconhecimento de voz
rec = sr.Recognizer()

# print(sr.Microphone().list_microphone_names()) <- lista os seus microfones

# é necessário iniciar o pyttsx3
iris = pyttsx3.init()

falar(iris, "Olá. Me chamo Iris, como posso ajudar?")
print("Iris >> Olá. Me chamo Iris, como posso ajudar?")
comando = ouvir(iris, rec)

while True:
    if "horas" in comando:
        horario = relogio(iris)

    elif "abrir" in comando or "abra" in comando or "abre" in comando:
        comando = formata_comando(comando)
        abrir(iris, comando)

    elif "pesquisar" in comando or "pesquise" in comando or "pesquisa" in comando:
        comando = formata_comando(comando)
        pesquisar(iris, rec, comando)

    # elif "previsão do tempo" in comando:
    #     cidade = formata_comando(comando)
    #     previsao_tempo(iris)

    elif comando == "não":
        falar(iris, f'Ok. Adeus...')
        print(f'Iris >> Ok.Adeus...')
        break

    falar(iris, "Mais alguma coisa?")
    print("Iris >> Mais alguma coisa?")
    comando = ouvir(iris, rec)
