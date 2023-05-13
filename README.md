# IRIS
Iris é um projeto do qual sempre tive vontade de fazer para aprender mais sobre como usar bibliotecas e APIs. Trata-se de uma Assistente Virtual (pessoal) que executa tarefas por comando de voz. Para que IRIS possa "ouvir" o que digo, utilizei a biblioteca SpeechRecognition, já para a sua fala usei o PYTTSX3, onde pude fazer algumas alterações em sua voz.

-- IRIS conta *ATUALMENTE* com as funções de relógio, pesquisar e de abrir:

Relógio: Um comando simples onde perguntamos as horas e ela responde o horário atual de brasília no formato (HH:MM). Para essa função utilizei a biblioteca DATETIME;

Pesquisar: Usando a biblioteca SELENIUM e o WEBDRIVER_MANAGER criei essa função que, por um comando de voz como "IRIS, pesquise por cursos de python", abre o navegador (chrome), digita na barra de pesquisa "cursos de python" e pesquisa. A janela do navegador fica aberta até que o comando de voz "fechar" seja acionado.

Abrir: Essa função abre aplicativos e jogos com a biblioteca SUBPROCESS. No arquivo "comandos.py" tem um dicionário onde estão os PATHS para os aplicativos que podem ser abertos, tais como Discord, Steam, Firefox e até o jogo League of Legends.

Além de adicionar mais comandos e melhorar a IRIS cada vez mais, meu maior desejo é trazer funções que a tornem uma IA

