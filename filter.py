import gzip
import json

with gzip.open('data.save.gz', 'r') as inf:
    data = json.load(inf)

print('input entries:', len(data))
new_data = [entry for entry in data if entry[1] > 24]
print('ouput entries:', len(new_data))

with gzip.open('data.save.gz', 'w') as outf:
    data_str = json.dumps(new_data)
    outf.write(data_str.encode('utf-8'))

