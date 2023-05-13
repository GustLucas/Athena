import datetime
import json
import requests
import speech_recognition as sr
import subprocess
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

paths = {
    # DAUNTLESS
    "dauntless": "C:\Program Files\Epic Games\Dauntless\Dauntless.exe",
    "downloads": "C:\Program Files\Epic Games\Dauntless\Dauntless.exe",
    "dá 13": "C:\Program Files\Epic Games\Dauntless\Dauntless.exe",
    "dá um 13": "C:\Program Files\Epic Games\Dauntless\Dauntless.exe",
    "não três": "C:\Program Files\Epic Games\Dauntless\Dauntless.exe",

    # LEAGUE OF LEGENDS
    "lol": "C:\Riot Games\Riot Client\RiotClientServices.exe",
    "uol": "C:\Riot Games\Riot Client\RiotClientServices.exe",
    "league of legends": "C:\Riot Games\Riot Client\RiotClientServices.exe",
    "liga das lendas": "C:\Riot Games\Riot Client\RiotClientServices.exe",

    # STEAM
    "steam": "C:\Program Files (x86)\Steam\steam.exe",
    "tim": "C:\Program Files (x86)\Steam\steam.exe",

    # EPIC
    "epic": "C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
    "epic games": "C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
    "epic games launcher": "C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",

    # FIREFOX
    "firefox": "C:\Program Files\Mozilla Firefox\firefox.exe",

    # CHROME
    "google": "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "chrome": "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": "C:\Program Files\Google\Chrome\Application\chrome.exe",

    # DISCORD
    #"discord": "C:\Users\gusta\AppData\Local\Discord\Update"

}


def falar(modelo, texto):
    rate = modelo.getProperty('rate')
    modelo.setProperty("rate", 200)  # define velocidade da fala

    voices = modelo.getProperty('voices')
    modelo.setProperty('voice', voices[0].id)  # seleciona a voz

    modelo.say(texto)
    modelo.runAndWait()


def ouvir(modelo, recognizer):
    with sr.Microphone(1) as mic:
        recognizer.adjust_for_ambient_noise(mic)  # se ajusa ao som ambiente (ruido)
        audio = recognizer.listen(mic)  # ouve o audio pelo microfone
        fala = ''
        try:
            fala = recognizer.recognize_google(audio, language="pt-BR").lower()  # converte o audio em texto
        except sr.UnknownValueError:  # recognizer não entendeu
            falar(modelo, "Desculpe, não entendi.")
        except sr.RequestError:
            falar(modelo, "Iris >> Desculpe, o serviço está offline.")

        print(f"Você>> {fala}")
        return fala


def relogio(modelo):
    horario = datetime.datetime.now().strftime("%H:%M")  # pega o horario atual e formata
    falar(modelo, f'Agora são {horario}')
    print(f'Iris >> Agora são {horario}.')


def pesquisar(modelo, rec, texto):
    falar(modelo, f"Pesquisando por {texto}")
    servico = Service(ChromeDriverManager().install())  # instala o serviço do webdriver
    navegador = webdriver.Chrome(service=servico)

    navegador.get("https://www.google.com/")

    barra_pesquisa = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'  # encontra o botão de
    navegador.find_element(By.XPATH, barra_pesquisa).send_keys(texto + Keys.ENTER)  # pesquisa e escreve nele

    while True:  # mantém o navegador aberto até ouvir o comando "fechar"
        time.sleep(1)
        comando = ouvir(modelo, rec)
        if "fechar" in comando:
            falar(modelo, "Fechando o google...")
            break


def abrir(modelo, app):
    try:
        program_path = paths[app]
        falar(modelo, f"Abrindo {app}")
        subprocess.Popen([program_path])
        time.sleep(1.5)

    except KeyError:
        falar(modelo, f"Desculpe. Não encontrei o aplicativo {app} no meu sistema.")
        time.sleep(0.5)


# def previsao_tempo(modelo, cidade="São+Paulo"):
#     chave_api = "a6c88e8d9ff7438de77da8eb6bbbd48e"
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&lang=pt_br&units=metric"
#
#     response = requests.get(url)
#     dados = json.loads(response.text)
#
#     temperatura = dados["main"]["temp"]
#     descricao = dados["weather"][0]["description"]
#
#     mensagem = f"A previsão do tempo para {cidade} é de {temperatura} graus Celsius, com {descricao}."
#     falar(modelo, mensagem)


def formata_comando(frase):
    comandos = ["pesquisar por", "pesquise por", "pesquisa aí", "abrir", "abra", "abrir o", "abrir a", "abra o", "abra a", "abre o"
                "abre a"]

    comandos = sorted(comandos, key=len, reverse=True)
    for comando in comandos:
        if comando in frase:
            posicao_comando = frase.find(comando)
            return frase[posicao_comando + len(comando):].strip()
    return frase
