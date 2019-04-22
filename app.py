from flask import Flask, render_template, request, url_for
import requests
import uuid
import time
import random

# Import Sequence CRDT
from static.crdt.sequence import Sequence

app = Flask(__name__)
seq = Sequence(uuid.uuid4())


@app.route("/")
def index():
    return render_template(
        'index.html')


@app.route("/insert/<elem>/")
def insert(elem):
    pos = int(request.args['pos'])
    global seq

    if pos < len(seq.id_seq):
        if pos == 0:
            seq.add(elem, seq.id_seq[pos] / 2)
        else:
            seq.add(elem, (seq.id_seq[pos - 1] + seq.id_seq[pos]) / 2)
    else:
        if pos == 0:
            if 0.5 in seq.id_remv_list:
                seq.add(elem, 0.5 + randrange_float(0.00000005, 0.000005, 0.00000005))
            else:
                seq.add(elem, 0.5)
        else:
            if pos in seq.id_remv_list:
                seq.add(elem, pos + randrange_float(0.00000005, 0.000005, 0.00000005))
            else:
                seq.add(elem, pos)
    print(seq.get_seq())
    return seq.get_seq()


@app.route("/remove/<pos>/")
def remove(pos):
    global seq
    if int(pos) <= len(seq.id_seq):
        id = seq.id_seq[int(pos) - 1]
        seq.remove(id)
    elif int(pos) == 0:
        pass

    print(seq.get_seq())
    return seq.get_seq()


@app.route("/update")
def update():
    # Call Merge function of other servers
    global seq
    port = request.host[-4:len(request.host)]
    for i in range(8000, 8002):
        if port != str(i):
            base_url = request.url_root[:-5] + str(i)
            merge_url = base_url + url_for('merge')
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

            # Send sequence object in call to other port
            r = requests.get(merge_url, json={'elem_list': seq.elem_list, 'id_remv_list': seq.id_remv_list},
                             headers=headers)

    return seq.get_seq()


@app.route("/merge")
def merge():
    global seq

    seq.merge(request.get_json()['elem_list'], 'elem')
    seq.merge(request.get_json()['id_remv_list'], 'id')

    print(seq.get_seq())
    return seq.get_seq()


@app.route('/get')
def get():
    global seq
    return seq.get_seq()


def get_time():
    return str(int(time.time_ns() / 100))


def create_unique_id(pos, frac):
    id = pos + float(frac / pow(10, len(str(frac))))
    return id


def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start


if __name__ == "__main__":
    app.run()
