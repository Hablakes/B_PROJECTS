import json    

data_test_0 = []
data_test_1 = []

with open(r'C:/Users/botoole/NEWTEST_MEDIA_INDEX/NEWTEST_USER_INFO.json') as f:
    a = json.load(f)
    print(a)

print('\n', '#' * 100, '\n')
for list_lines in data_test_0:
    print(list_lines)
