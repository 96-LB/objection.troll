import os, base64, json
from merge import merge
from process import process

PATH = 'input'
TEMP = 'temp'
OUT = '.out.objection'

if not os.path.exists(PATH):
    os.mkdir(PATH)

if not os.path.exists(TEMP):
    os.mkdir(TEMP)


data = []
files = sorted(os.listdir(PATH), key=lambda x: x.lower())

for filename in files:
    with open(os.path.join(PATH, filename)) as file:
        data.append(json.loads(base64.b64decode(file.read())))

        file.seek(0)
        with open(os.path.join(TEMP, filename), 'wb') as temp:
            temp.write(base64.b64decode(file.read()))


out = process(merge(data))

with open(os.path.join(TEMP, OUT), 'w') as temp:
    temp.write(json.dumps(out))

with open(OUT, 'wb') as file:
    file.write(base64.b64encode(json.dumps(out).encode('utf8')))

print('done!')
