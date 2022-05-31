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

# Auxiliary Functions
def input_validate(input_value):
    while True:
        if (input_value.isnumeric() and eval(input_value) in [0,1,2,3,4]):
            return eval(input_value)
        else:
            input_value  = input('Digite um valor válido: ')

def create_dir():
    try:
        if "./Análise":
            os.makedirs("./Análise")
    except OSError:
        ...

def write_to_file(file_name, content, op):
    create_dir()
    with open(file_name, op) as file:
        file.write(content)
# --------------------------------------


def requests_answered():

    access_log = open('access.log', 'r')

    for request in access_log:
        http_object_regex = re.compile(r'2\d\d [0-9]{4,9}')
        http_object_regex_ok = http_object_regex.findall(request)

        if http_object_regex_ok and eval(http_object_regex_ok[0][3::]) > 2000:
            ip_regex = re.compile(r'\d*\.\d*\.\d*\.\d* ')
            dados_ip = ip_regex.findall(request)

            response = (f'{http_object_regex_ok[0]} {dados_ip[0]}\n')
            write_to_file("./Análise/respondidosNovembro.txt", response, "a+")

    access_log.close() 

def not_requests_answered():
    regex_bad_request = re.compile(r" 4[0-9]{2} ")
    regex_date = re.compile(r'[0-9]{2}/Nov/2021:[0-9]{2}:[0-9]{2}:[0-9]{2} [+][0-9]{4}')
    regex_address = re.compile(r"(\"http://)(.*?)(\")")

    access_log = open("access.log", "r")

    for request in access_log:
        http_bad_request = regex_bad_request.findall(request)
        request_date = regex_date.findall(request)

        if http_bad_request and request_date:
            request_address = regex_address.findall(request)
            response = ""

            if request_address:
                address = "".join(request_address[0])
                if(address != ""):
                    response = (
                        http_bad_request[0].strip() + " " + address + " " + request_date[0] + "\n"
                    )

            write_to_file("./Análise/nãoRespondidosNovembro.txt", response, "a+")

    access_log.close()

def requests_by_operational_system():

    def take_operational_system_percentage(operational_system_quantitative):
        number_of_requests = len(os.popen('cat access.log').readlines()) 
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
        "Mobile" : 0
    }

    linux_and_others = 0

    for request in access_log:
        if(re.findall(data_2021_regex, request)):
            for system in operational_systems:
                if(system == "Linux"):
                    if((re.compile(r'X11').findall(request))):
                        for sub_system in sub_linux_x11:
                            if(sub_system in request):
                                sub_linux_x11[sub_system] += 1
                            else:
                                linux_and_others += 1
                    elif(re.compile(fr"{system}; Android").findall(request) or re.compile(r";Mobile;").findall(request)):
                        sub_linux_mobile["Mobile"] += 1
                else:
                    if(re.findall(fr'{system}', request)):
                        operational_systems[system] += 1
    access_log.close()

    table_of_percent = {

        "Windows" : operational_systems["Windows"],
        "Macintosh" : operational_systems["Macintosh"],
        "Ubuntu" : sub_linux_x11["Ubuntu"],
        "Fedora" : sub_linux_x11["Fedora"],
        "Mobile" : sub_linux_mobile["Mobile"],
        "Linux, outros" : linux_and_others
    }

    response = ""

    for line_content in table_of_percent:
        response += (f'{line_content} {take_operational_system_percentage(table_of_percent[line_content])}\n')
    
    write_to_file("./Análise/requestsPorSistemaOperacional.txt", response, "w+")
    

def average_requests_post():
    access_log = open('../access.log', 'r')

    req_post_regex = re.compile(r'POST')

    total_post_requests_with_success = 0
    sum_of_all_post_requests_with_success_length = 0

    for request in access_log:
        if((re.findall(data_2021_regex, request)) and (req_post_regex.findall(request))):
            if(re.compile(r'2[0-9]{2} [0-9]{1,9}').findall(request)):
                total_post_requests_with_success += 1
                response = request.split('"')
                state_and_length = response[2].strip().split()
                sum_of_all_post_requests_with_success_length += int(state_and_length[1])

    access_log.close()
    average_of_all_post_requests_with_success = sum_of_all_post_requests_with_success_length / total_post_requests_with_success
    print(f"Média das requisições POST de 2021 respondidas com sucesso: {average_of_all_post_requests_with_success}")

def menu():

    execution_Condition = True

    while (execution_Condition):

        menu_option = input_validate(input("""
    1 - Recursos grandes respondidos
    2 - Não respondidos
    3 - "%" de requisições por SO
    4 - Média das requisições POST
    0 - Sair
    Digite a opção desejada: """))

        match menu_option:
            case 1:
                requests_answered()
            case 2:
                not_requests_answered()
            case 3:
                requests_by_operational_system()
            case 4:
                average_requests_post()
            case 0:
                execution_Condition = False

if __name__ == '__main__':
    menu()
