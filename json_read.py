import json

with open('speedbump_static_2.json', 'r') as f:
    data = json.load(f)
# print(data.keys())

f = open('data_json.txt', 'w')
for key in data.keys():
    f.write('\"' + key + '\"' + ',' + '\n')
    # f.write(key + '\n')

f.close()

