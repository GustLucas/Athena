from ATHENA import Athena

athena = Athena()

while True:
    comando = athena.aguarda_comando()
    if "horas" in comando:
        horario = athena.relogio()

    elif "data" in comando or "dia" in comando:
        athena.data()

    elif "abrir" in comando or "abra" in comando or "abre" in comando:
        comando = athena.formata_comando(comando)
        athena.abrir(comando)

    elif "pesquisar" in comando or "pesquise" in comando or "pesquisa" in comando:
        comando = athena.formata_comando(comando)
        athena.pesquisar(comando)

    elif "curiosidade" in comando:
        athena.buscar_curiosidade()

