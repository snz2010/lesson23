import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def query_builder(it, cmd, val):
    result = map(lambda v: v.strip(), it)
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




@app.route("/perform_query", methods=["POST"])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    try:
        cmd1 = request.args["cmd1"]
        cmd2 = request.args["cmd2"]
        val1 = request.args["val1"]
        val2 = request.args["val2"]
        file_name = request.args["file_name"]
    except KeyError:
        raise BadRequest(description="не все параметры переданы корректно")


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