import json    

data_test_0 = []
data_test_1 = []

with open(r'C:/Users/botoole/TEST_MEDIA_INDEX/TEST_USER_INFO.json') as f:
    for line in f:
        data_test_0.append(line)

for items in data_test_0:
    print(items)
