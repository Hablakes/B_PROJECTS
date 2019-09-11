import json    

data_test_0 = []
data_test_1 = []

with open(r'C:/Users/botoole/NEWTEST_MEDIA_INDEX/NEWTEST_USER_INFO.json') as f:
    a = json.load(f)
    print(a)
    print('\n', '#' * 100, '\n')
    print(a['user:'])
    print('\n', '#' * 100, '\n')
    print(a['movie_dir:'])
    print('\n', '#' * 100, '\n')
    print(a['tv_dir:'])
    print('\n', '#' * 100, '\n')
    print(a['movie_alt_dir:'])
    print('\n', '#' * 100, '\n')
    print(a['tv_alt_dir:'])
    print('\n', '#' * 100, '\n')
