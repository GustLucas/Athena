from Imports import *


class Athena:
    def __init__(self):
        self.rec = sr.Recognizer()  # reconhecedor de voz
        self.engine = pyttsx3.init()  # inicializar o mecanismo de síntese de fala:
        self.servico = Service(ChromeDriverManager().install())  # instala o serviço do webdriver
        self.ola()

    def aguarda_comando(self):
        if keyboard.is_pressed('ctrl+alt'):
            comando = self.ouvir()
            return comando

    def falar(self, texto):
        rate = self.engine.getProperty('rate')
        self.engine.setProperty("rate", 200)  # define a velocidade da fala

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # seleciona a voz

        self.engine.say(texto)
        self.engine.runAndWait()
        print("Athena >> " + texto)

    def ouvir(self):
        recognizer = self.rec
        self.falar('Estou ouvindo...')
        with sr.Microphone(1) as mic:
            recognizer.adjust_for_ambient_noise(mic)    # se ajusta ao som ambiente (ruído)
            audio = recognizer.listen(mic, 5)  # ouve o audio pelo microfone
            fala = ''
            try:
                fala = recognizer.recognize_google(audio, language="pt-BR").lower() # converte o audio em texto
            except sr.UnknownValueError:
                self.falar('Desculpe, não entendi.')
            except sr.RequestError:
                self.falar('Desculpe, o serviço está offline.')

            print('Você >> ' + fala)
            return fala

    def relogio(self):
        horario = datetime.datetime.now().strftime('%H:%M')     # pega o horário atual e formata
        self.falar('Agora são ' + horario)

    def data(self):
        meses = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }

        ano = int(datetime.datetime.now().year)
        mes = int(datetime.datetime.now().month)
        dia = int(datetime.datetime.now().day)

        self.falar(f'Hoje é dia {dia} de {meses[mes]} de {ano}')

    def ola(self):
        self.falar("Olá! Me chamo Athena.")
        self.data()
        self.relogio()
        self.falar("Como posso ajudá-lo?")

    # def pesquisar(self, texto):
    #     self.falar('Pesquisando por ' + texto)
    #     navegador = webdriver.Chrome(service=self.servico)
    #
    #     navegador.get('https://www.google.com/')
    #     barra_pesquisa = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'
    #     navegador.find_element(By.XPATH, barra_pesquisa).send_keys(texto + Keys.ENTER)

    def pesquisar(self, texto):
        self.falar('Pesquisando por ' + texto)
        navegador = webdriver.Chrome(service=self.servico)

        try:
            navegador.get('https://www.google.com/')
            barra_pesquisa = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'
            navegador.find_element(By.XPATH, barra_pesquisa).send_keys(texto + Keys.ENTER)

            input("Pressione Enter para fechar o navegador...")  # Aguarda ação do usuário

        finally:
            navegador.quit()  # Fecha o navegador ao finalizar

    def abrir(self, app):
        try:
            program_path = paths[app]
            self.falar('Claro! Abrindo ' + app)
            subprocess.Popen([program_path])
            time.sleep(1.5)

        except KeyError:
            self.falar(f"Desculpe. Não encontrei o aplicativo {app} no meu sistema.")
            time.sleep(0.5)

    def formata_comando(self, frase):
        # comandos que podem ser usados
        comandos = ["pesquisar por", "pesquise por", "pesquisa aí", "abrir", "abra", "abrir o", "abrir a", "abra o",
                    "abra a", "abre o", "abre a"]

        comandos = sorted(comandos, key=len, reverse=True)
        for comando in comandos:
            if comando in frase:
                posicao_comando = frase.find(comando)
                return frase[posicao_comando + len(comando):].strip()
        return frase

    def buscar_curiosidade(self):
        self.falar("Claro! Aqui vai uma curiosidade aleatória.")
        # Faz uma requisição à API do Wikipedia para buscar uma página aleatória
        requisicao = requests.get('https://pt.wikipedia.org/w/api.php?action=query&format=json&list=random&rnnamespace='
                                  '0&rnlimit=1')

        # Extrai o título da página aleatória a partir da resposta da API
        titulo_pagina = requisicao.json()['query']['random'][0]['title']

        # Faz uma nova requisição à API para buscar o conteúdo da página
        requisicao = requests.get(
            f'https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=1&ex'
            f'plaintext=1&titles={titulo_pagina}')

        # Extrai o texto do primeiro parágrafo do conteúdo da página
        conteudo_pagina = requisicao.json()['query']['pages']
        id_primeira_pagina = next(iter(conteudo_pagina))
        primeiro_paragrafo = conteudo_pagina[id_primeira_pagina]['extract'].split('\n')[0]

        # Remove referências numéricas e tags HTML do texto
        primeiro_paragrafo = re.sub(r'\[[0-9]+]', '', primeiro_paragrafo)
        primeiro_paragrafo = re.sub(r'<[^>]*>', '', primeiro_paragrafo)

        curiosidade = primeiro_paragrafo.strip()
        self.falar(curiosidade)

