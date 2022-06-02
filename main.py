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

# Libraries Imports
import re
import os
import time

# Tools
date_2021_regex = re.compile(r"[0-9]{2}/[A-Z][a-z]{2}/2021:[0-9]{2}:[0-9]{2}:[0-9]{2} [+][0-9]{4}")
http_continue_status_regex = re.compile(r"2\d\d [0-9]{4,9}")


# Auxiliary Functions
def input_validate(input_value):
    condition = True
    while condition:
        valid_inputs = [0, 1, 2, 3, 4]
        if input_value.isnumeric() and (eval(input_value) in valid_inputs):
            return eval(input_value)
        else:
            input_value = input("Digite um valor válido: ")


def create_dir():
    try:
        if "./Análise":
            os.makedirs("./Análise")
    except OSError:
        ...


def write_to_file(file_name, content, op):
    create_dir()
    with open(file_name, op) as file:
        file.writelines(content)


def clean():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


def big_requests_answered():
    initial_time = time.time()
    print("Executando...")

    ip_regex = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    response = []

    access_log = open("access.log", "r")

    for request in access_log:
        http_continue_status_regex_ok = http_continue_status_regex.findall(request)

        if http_continue_status_regex_ok and eval(http_continue_status_regex_ok[0][3::]) > 2000:
            ip_data = ip_regex.findall(request)

            response.append(http_continue_status_regex_ok[0] + ip_data[0] + '\n')

    write_to_file('./Análise/recursosGrandes.txt', response, 'w+')
    clean()
    print(f"Tempo de Execução {time.time() - initial_time:.2f}\n")
    access_log.close()


def not_answered_requests():
    initial_time = time.time()
    print("Executando...")

    regex_bad_request = re.compile(r" 4[0-9]{2} ")
    regex_date = re.compile(r"[0-9]{2}/Nov/2021:[0-9]{2}:[0-9]{2}:[0-9]{2} [+][0-9]{4}")
    regex_address = re.compile(r"(\"http://)(.*?)(\")")
    response = []

    access_log = open("access.log", "r")

    for request in access_log:
        http_bad_request = regex_bad_request.findall(request)
        request_date = regex_date.findall(request)

        if http_bad_request and request_date:
            request_address = regex_address.findall(request)

            if request_address:
                address = "".join(request_address[0])
                if (address != ""):
                    response.append(
                            http_bad_request[0].strip() + " " + address + " " + request_date[0] + "\n"
                    )

    
    write_to_file("./Análise/nãoRespondidosNovembro.txt", response, "w+")
    clean()
    print(f"Tempo de Execução {time.time() - initial_time:.2f}\n")
    access_log.close()


def requests_by_operational_system():
    initial_time = time.time()
    print("Executando...")

    def take_operational_system_percentage(operational_system_quantitative):
        number_of_requests = len(os.popen("cat access.log").readlines())
        percentage = (operational_system_quantitative / number_of_requests) * 100
        return percentage

    access_log = open("access.log", "r")

    operational_systems = {
        "Windows": 0,
        "Linux": 0,
        "Macintosh": 0,
    }

    sub_linux_x11 = {
        "Ubuntu": 0,
        "Fedora": 0,
    }

    sub_linux_mobile = {
        "Mobile": 0
    }

    linux_and_others = 0

    for request in access_log:
        if (re.findall(date_2021_regex, request)):
            for system in operational_systems:
                if (system == "Linux"):
                    if ((re.compile(r'X11').findall(request))):
                        for sub_system in sub_linux_x11:
                            if (sub_system in request):
                                sub_linux_x11[sub_system] += 1
                            else:
                                linux_and_others += 1
                    elif (re.compile(fr"{system}; Android").findall(request) or re.compile(r";Mobile;").findall(
                            request)):
                        sub_linux_mobile["Mobile"] += 1
                else:
                    if (re.findall(fr"{system}", request)):
                        operational_systems[system] += 1
    access_log.close()

    table_of_percent = {

        "Windows": operational_systems["Windows"],
        "Macintosh": operational_systems["Macintosh"],
        "Ubuntu": sub_linux_x11["Ubuntu"],
        "Fedora": sub_linux_x11["Fedora"],
        "Mobile": sub_linux_mobile["Mobile"],
        "Linux, outros": linux_and_others
    }

    response = ""

    for line_content in table_of_percent:
        response += (f'{line_content} {take_operational_system_percentage(table_of_percent[line_content])}\n')

    clean()
    print(f"Tempo de Execução {time.time() - initial_time:.2f}\n")
    write_to_file("./Análise/requestsPorSistemaOperacional.txt", response, "w+")


def average_requests_post():
    initial_time = time.time()
    print("Executando...")
    access_log = open("./access.log", "r")

    req_post_regex = re.compile(r"POST")

    total_post_requests_with_success = 0
    sum_of_all_post_requests_with_success_length = 0


    for request in access_log:
        http_status_data = http_continue_status_regex.findall(request)
        if re.findall(date_2021_regex, request) and req_post_regex.findall(request) and http_status_data:
            total_post_requests_with_success += 1
            response = request.split('"')
            http_status, request_size = http_status_data[0].split()
            sum_of_all_post_requests_with_success_length += int(request_size)

    clean()
    print(f"Tempo de Execução {time.time() - initial_time:.2f}\n")
    access_log.close()
    average_of_all_post_requests_with_success = sum_of_all_post_requests_with_success_length / total_post_requests_with_success
    print(f"Média das requisições POST de 2021 respondidas com sucesso: {average_of_all_post_requests_with_success:.2f}")


def menu():
    execution_Condition = True
    while (execution_Condition):
        menu_option = input_validate(input("""1 - Recursos grandes respondidos
2 - Não respondidos
3 - "%" de requisições por SO
4 - Média das requisições POST
0 - Sair\n
Digite a opção desejada: """))

        match menu_option:
            case 1:
                big_requests_answered()
            case 2:
                not_answered_requests()
            case 3:
                requests_by_operational_system()
            case 4:
                average_requests_post()
            case 0:
                execution_Condition = False


if __name__ == '__main__':
    menu()
