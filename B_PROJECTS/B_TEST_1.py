import json    

data_test_0 = []
data_test_1 = []

with open(r'C:/Users/botoole/TEST_MEDIA_INDEX/TEST_USER_INFO.json') as f:
    for json_lines in f:
        data_test_0.append(json_lines)
        print(json.dumps(json_lines))

print('\n', '#' * 100, '\n')
for list_lines in data_test_0:
    print(list_lines)
