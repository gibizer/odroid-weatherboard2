import gzip
import json

with gzip.open('data.save.gz', 'r') as inf:
    data = json.load(inf)

print('input entries:', len(data))
new_data = [entry for entry in data if entry[1] > 17.0]
new_data = [entry for entry in new_data if entry[2] > 30.0]
new_data = [entry for entry in new_data if entry[3] > 70000]

temp = [entry[1] for entry in data]
hum = [entry[2] for entry in data]
press = [entry[3] for entry in data]
print('temp', min(temp), max(temp))
print('hum', min(hum), max(hum))
print('press', min(press), max(press))
print('--- new')
temp = [entry[1] for entry in new_data]
hum = [entry[2] for entry in new_data]
press = [entry[3] for entry in new_data]
print('temp', min(temp), max(temp))
print('hum', min(hum), max(hum))
print('press', min(press), max(press))

#new_data = []
#for entry in data:
#    if entry[2] > 48:
#        entry[2] = entry[2] - 10
#    new_data.append(entry)

# new_data = data[:-10]
 
print('ouput entries:', len(new_data))

with gzip.open('data.save.gz', 'w') as outf:
    data_str = json.dumps(new_data)
    outf.write(data_str.encode('utf-8'))

