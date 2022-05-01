import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

""" В ФП функции должны принимать входные данные, обрабатывать их и возвращать выходные данные, 
при этом не должны иметь какого-либо внутреннего состояния, которое будет влиять на результат.
Функция должна всегда возвращать одинаковый результат при одинаковых входных данных.
Это — фундаментальная концепция ФП """


def query_builder(iterable_var, cmd, val):
    result = map(lambda v: v.strip(), iterable_var)
    if cmd == "filter":
        result = filter(lambda v, txt=val: txt in v, result)
    if cmd == "map":
        arg = int(val)
        result = map(lambda v, idx=arg: v.split(" ")[idx], result)
    if cmd == "unique":
        result = set(result)
    if cmd == "sort":
        reverse = val == "desc"
        result = sorted(result, reverse=reverse)
    if cmd == "limit":
        arg = int(val)
        result = list(result)[:arg]
    return result


def get_commands(query):
    cmd = []
    arg = []
    query_items = query.split("|")
    for item in query_items:
        if item == 'unique':
            cmd.append('unique')
            arg.append('')
        elif 'file_name' in item:
            filename = item.split(":")[1]
        else:
            split_item = item.split(":")
            print(split_item)
            cmd.append(split_item[0])
            arg.append(split_item[1])
    ret_list = list(zip(cmd, arg))
    return ret_list, filename



@app.route("/perform_query", methods=["POST", "GET"])
def perform_query():
    if request.method == "POST":
        # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
        try:
            cmd1 = request.args["cmd1"]
            cmd2 = request.args["cmd2"]
            val1 = request.args["val1"]
            val2 = request.args["val2"]
            file_name = request.args["file_name"]
        except KeyError:
            raise BadRequest(description="не все параметры переданы корректно")
    elif request.method == "GET":
        query_str = request.args.get("query")
        ret_list, file_name = get_commands(query_str)
        (cmd1, val1) = ret_list[0]
        (cmd2, val2) = ret_list[1]

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"файл {file_name} не найден")

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    with open(file_path) as f:
        res = query_builder(f, cmd1, val1)
        res = query_builder(res, cmd2, val2)
        content = '\n'.join(res)
        print(content)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run()
