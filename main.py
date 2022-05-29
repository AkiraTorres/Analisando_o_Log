#
#   -------------------------------------------------------------------------------------------------
#   |   Alunos :                                                                                    |
#   |                                                                                               |
#   |       - Júlio Cesar Roque da Silva                                                            |
#   |       - José Gustavo de Oliveira Cunha                                                        |
#   |       - José Thiago Torres da Silva                                                           |
#   |       - João Victor Mendes de Lira                                                            |
#   |       - Gabriel Valdormiro da Silva                                                           |
#   -------------------------------------------------------------------------------------------------
#

#Importação de bibliotecas
import re 
import os

def recursosGrandesRespondidos():

    access_log = open('access.log', 'r')

    for registros in access_log:
        http_objeto_regex = re.compile(r'2\d\d [0-9]{4,9}')
        http_objeto_ok = http_objeto_regex.findall(registros)

        if http_objeto_ok and eval(http_objeto_ok[0][3::]) > 2000:
            IP_regex = re.compile(r'\d*\.\d*\.\d*\.\d* ')
            dados_IP = IP_regex.findall(registros)

            with open('./Análise/recursosGrandes.txt', 'a+') as recursosGrandes:
                recursosGrandes.write(f'{http_objeto_ok[0]} {dados_IP[0]}\n')

    access_log.close() 

def requisicoesPorSistemaOperacional():

    WindowsRegex = re.compile(r'Windows')
    MacintoshRegex = re.compile(r'Macintosh')
    LinuxRegex = re.compile(r'Linux')
    x11Regex = re.compile(r'X11')
    FedoraRegex = re.compile(r'Fedora')
    AndroidRegex = re.compile(r'Android')
    MobileRegex = re.compile(r'Mobile')

    sistemasOperacionais = {

            "Windows" : 0,
            "Macintosh" : 0,
            "Ubuntu" : 0,
            "Fedora" : 0,
            "Mobile" : 0,
            "Linux, outros" : 0

        }

    access_log = open('access.log', 'r')



    for registro in access_log:
        SistemasOperacionaisAnoRegex = re.compile(r'\d\d/[A-Z][a-z][a-z]/2021:\d\d:\d\d:\d\d [+]\d\d\d\d')
        http_objeto_ok = SistemasOperacionaisAnoRegex.findall(registro)

        if(http_objeto_ok):

            if(MacintoshRegex.findall(registro)):
                sistemasOperacionais["Macintosh"] += 1
            elif(WindowsRegex.findall(registro)):
                sistemasOperacionais["Windows"] += 1
            elif(FedoraRegex.findall(registro)):
                sistemasOperacionais["Fedora"] += 1
            elif(AndroidRegex.findall(registro)):
                sistemasOperacionais["Mobile"] += 1
            elif(MobileRegex.findall(registro)):
                sistemasOperacionais["Mobile"] += 1
            elif(LinuxRegex.findall(registro)):
                if(x11Regex.findall(registro)):
                    sistemasOperacionais["Linux, outros"] += 1
                else:
                    sistemasOperacionais["Ubuntu"] += 1

    access_log.close() 

    aux = open("./Análise/sistemaOperacionais.txt", "w")
    for sistema in sistemasOperacionais:
        aux.write(f'{sistema} {(sistemasOperacionais[sistema]/1000000)*100}\n')
    

def media_requisicoes_post():
    log = open('../access.log', 'r')

    req_post_regex = re.compile(r'POST')
    date_regex = re.compile(r'2021')

    response_size_total = 0
    total_responses = 0

    for data in log:
        date = date_regex.findall(data)
        request = req_post_regex.findall(data)

        if date and request:
            total_responses += 1
            response = data.split('"')
            response_size = response[2].strip().split()
            response_size_total += int(response_size[1])

    log.close()
    print(f"Média das requisições POST de 2021 respondidas com sucesso: {response_size_total/total_responses}")

def naoRespondidos():
    regexBadRequest = re.compile(r" 4\d\d ")
    regexDate = re.compile(r"Nov/2021")
    regexAddress = re.compile(r"(\"http://)(.*?)(\")")

    log = open("access.log", "r")

    for data in log:
        httpBadRequest = regexBadRequest.findall(data)
        requestDate = regexDate.findall(data)

        if httpBadRequest and requestDate:
            requestAddress = regexAddress.findall(data)
            response = ""

            if requestAddress:
                address = "".join(requestAddress[0])
                response = (
                    httpBadRequest[0].strip() + " " + address + " " + requestDate[0] + "\n"
                )
            else:
                response = httpBadRequest[0].strip() + ' "-" ' + requestDate[0] + "\n"

            with open(
                "./Análise/naoRespondidosNovembro.txt", "a+"
            ) as naoRespondidosNovembro:
                naoRespondidosNovembro.write(response)


    log.close()

def validarEntrada(valorDeEntrada):
        while (True):
            if(valorDeEntrada not in [0,1,2,3,4]):
                print("Opção inválida, tente novamente")
                valorDeEntrada = int(input("Digite novamente a opção desejada: "))
            else:
                return valorDeEntrada

def criarPasta():

    try:
        if "./Análise":
            os.makedirs("./Análise")
    except OSError:
        ...

while (True):

    print("""
1 - Recursos grandes respondido
2 - Não respondidos
3 - "%" de requisições por SO
4 - Média das requisições POST
0 - Sair

""")

    criarPasta()
    opcao = validarEntrada(int(input("Digite a opção desejada: ")))

    match opcao:
        case 1:
            recursosGrandesRespondidos()
        case 2:
            naoRespondidos()
        case 3:
            requisicoesPorSistemaOperacional()
        case 4:
            media_requisicoes_post()
        case 0:
            break