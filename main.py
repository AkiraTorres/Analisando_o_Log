#
#   -------------------------------------------------------------------------------------------------
#   |   Alunos :                                                                                    |
#   |                                                                                               |
#   |       - Júlio Cesar Roque da Silva                                                            |
#   |       - José Gustavo de Oliveira Cunha                                                        |
#   |       - José Thiago Torres da Silva                                                           |
#   |       - João Victor Mendes de Lira                                                            |
#   |       - Gabriel Valdomiro da Silva                                                           |
#   -------------------------------------------------------------------------------------------------
#

# Importação de bibliotecas
import os
import re


def big_requests_answered():
    log = open('access.log', 'r')

    http_object_regex = re.compile(r'2\d\d \d{4,9}')
    ip_regex = re.compile(r'\d*\.\d*\.\d*\.\d* ')

    for data in log:
        http_object_ok = http_object_regex.findall(data)

        if http_object_ok and eval(http_object_ok[0][3::]) > 2000:
            dados_ip = ip_regex.findall(data)

            with open('./Análise/recursosGrandes.txt', 'w+') as big_resources:
                big_resources.write(f'{http_object_ok[0]} {dados_ip[0]}\n')

    log.close()


def requests_by_os():
    windows_regex = re.compile(r'Windows')
    macintosh_regex = re.compile(r'Macintosh')
    linux_regex = re.compile(r'Linux')
    x11_regex = re.compile(r'X11')
    fedora_regex = re.compile(r'Fedora')
    android_regex = re.compile(r'Android')
    mobile_regex = re.compile(r'Mobile')

    operational_systems = {

        "Windows": 0,
        "Macintosh": 0,
        "Ubuntu": 0,
        "Fedora": 0,
        "Mobile": 0,
        "Linux, outros": 0

    }

    log = open('access.log', 'r')

    for data in log:
        date_regex = re.compile(r'\d\d/[A-Z][a-z][a-z]/2021:\d\d:\d\d:\d\d [+]\d\d\d\d')
        http_status = date_regex.findall(data)

        if http_status:

            if macintosh_regex.findall(data):
                operational_systems["Macintosh"] += 1
            elif windows_regex.findall(data):
                operational_systems["Windows"] += 1
            elif fedora_regex.findall(data):
                operational_systems["Fedora"] += 1
            elif android_regex.findall(data):
                operational_systems["Mobile"] += 1
            elif mobile_regex.findall(data):
                operational_systems["Mobile"] += 1
            elif linux_regex.findall(data):
                if x11_regex.findall(data):
                    operational_systems["Linux, outros"] += 1
                else:
                    operational_systems["Ubuntu"] += 1

    log.close()

    aux = open("./Análise/sistemaOperacionais.txt", "w+")
    for sistema in operational_systems:
        aux.write(f'{sistema} {(operational_systems[sistema] / 1000000) * 100}\n')


def media_requests_post():
    log = open('access.log', 'r')

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
    print(f"Média das requisições POST de 2021 respondidas com sucesso: {response_size_total / total_responses}")


def not_answered_requests():
    regex_bad_request = re.compile(r" 4\d\d ")
    regex_date = re.compile(r"Nov/2021")
    regex_address = re.compile(r"(\"http://)(.*?)(\")")

    log = open("access.log", "r")

    for data in log:
        http_bad_request = regex_bad_request.findall(data)
        request_date = regex_date.findall(data)

        if http_bad_request and request_date:
            request_address = regex_address.findall(data)

            if request_address:
                address = "".join(request_address[0])
                response = (
                        http_bad_request[0].strip() + " " + address + " " + request_date[0] + "\n"
                )
            else:
                response = http_bad_request[0].strip() + ' "-" ' + request_date[0] + "\n"

            with open(
                    "./Análise/naoRespondidosNovembro.txt", "w+"
            ) as not_answered_nov:
                not_answered_nov.write(response)

    log.close()


def validate_input(input_value):
    n = True

    while n:
        if input_value not in ["0", "1", "2", "3", "4"]:
            print("Opção inválida, tente novamente")
            input_value = input("Digite novamente a opção desejada: ")
        else:
            return input_value


def create_dir():
    try:
        if "./Análise":
            os.makedirs("./Análise")
    except OSError:
        ...


def menu():
    n = True

    while n:
        print("""
        1 - Recursos grandes respondido
        2 - Não respondidos
        3 - "%" de requisições por SO
        4 - Média das requisições POST
        0 - Sair
        """)

        create_dir()
        input_value = validate_input(input("Digite a opção desejada: "))

        match input_value:
            case "1":
                big_requests_answered()
            case "2":
                not_answered_requests()
            case "3":
                requests_by_os()
            case "4":
                media_requests_post()
            case "0":
                n = False


if __name__ == '__main__':
    menu()
