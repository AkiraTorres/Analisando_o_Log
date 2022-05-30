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

# Libraries Imports
import re 
import os
# --------------------------------------

# Tools
data_2021_regex = re.compile(r'[0-9]{2}/[A-Z][a-z]{2}/2021:[0-9]{2}:[0-9]{2}:[0-9]{2} [+][0-9]{4}')
# --------------------------------------


def input_validate(value):

    while True:
        if value.isnumeric() and eval(value) in [0,1,2,3,4]:
            return eval(value)
        else:
            value  = input('Digite um valor válido: ')

def create_dir():

    try:
        if "./Análise":
            os.makedirs("./Análise")
    except OSError:
        ...

def requests_answered():

    access_log = open('access.log', 'r')

    for registry in access_log:
        http_object_regex = re.compile(r'2\d\d [0-9]{4,9}')
        http_object_regex_ok = http_object_regex.findall(registry)

        if http_object_regex_ok and eval(http_object_regex_ok[0][3::]) > 2000:
            IP_regex = re.compile(r'\d*\.\d*\.\d*\.\d* ')
            dados_IP = IP_regex.findall(registry)

            with open('./Análise/recursosGrandes.txt', 'a+') as large_resources:
                large_resources.write(f'{http_object_regex_ok[0]} {dados_IP[0]}\n')

    access_log.close() 

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

def requests_by_operational_system():

    def take_operational_system_percentage(operational_system_quantitative):
        number_of_requests = 1000000
        percentage = (operational_system_quantitative / number_of_requests) * 100
        return percentage

    access_log = open('access.log', 'r')

    operational_systems = {
        "Windows" : 0,
        "Linux" : 0,
        "Macintosh" : 0,
    }

    sub_linux_x11 = {
        "Ubuntu" : 0,
        "Fedora" : 0,
    }

    sub_linux_mobile = {
        "Android" : 0,
        "Mobile" : 0,
    }

    linux_and_others = 0

    for registry in access_log:
        if(re.findall(data_2021_regex, registry)):
            for system in operational_systems:
                if(system == "Linux"):
                    if((re.compile(r'X11').findall(registry))):
                        for sub_system in sub_linux_x11:
                            if(sub_system in registry):
                                sub_linux_x11[sub_system] += 1
                            else:
                                linux_and_others += 1
                    elif(re.compile(fr"{system}; Android").findall(registry) or re.compile(r";Mobile;").findall(registry)):
                        sub_linux_mobile["Mobile"] += 1
                else:
                    if(re.findall(fr'{system}', registry)):
                        operational_systems[system] += 1
    access_log.close()

    table_of_percent = {

        "Windows" : operational_systems["Windows"],
        "Macintosh" : operational_systems["Macintosh"],
        "Ubuntu" : sub_linux_x11["Ubuntu"],
        "Fedora" : sub_linux_x11["Fedora"],
        "Mobile" : sub_linux_mobile["Mobile"] + sub_linux_mobile["Android"],
        "Linux, outros" : linux_and_others
    }

    aux = open("./Análise/sistemaOperacionais.txt", "w")
    for line_content in table_of_percent:
        aux.write(f'{line_content} {take_operational_system_percentage(table_of_percent[line_content])}\n')
    

def average_requests_post():
    log = open('../access.log', 'r')

    req_post_regex = re.compile(r'POST')

    total_post_requests_with_success = 0
    sum_of_all_post_requests_with_success_length = 0

    for registry in log:
        if((re.findall(data_2021_regex, registry)) and (req_post_regex.findall(registry))):
            if(re.compile(r'2[0-9]{2} [0-9]{1,9}').findall(registry)):
                total_post_requests_with_success += 1
                response = registry.split('"')
                state_and_length = response[2].strip().split()
                sum_of_all_post_requests_with_success_length += int(state_and_length[1])

    log.close()
    average_of_all_post_requests_with_success = sum_of_all_post_requests_with_success_length / total_post_requests_with_success
    print(f"Média das requisições POST de 2021 respondidas com sucesso: {average_of_all_post_requests_with_success}")

def menu():

    execution_Condition = True

    while (execution_Condition):

        menu_option = input_validate(input("""

    1 - Recursos grandes respondido
    2 - Não respondidos
    3 - "%" de requisições por SO
    4 - Média das requisições POST
    0 - Sair

    Digite a opção desejada: """))

        create_dir()

        match menu_option:
            case 1:
                requests_answered()
            case 2:
                naoRespondidos()
            case 3:
                requests_by_operational_system()
            case 4:
                average_requests_post()
            case 0:
                execution_Condition = False

if __name__ == '__main__':
    menu()
