test_strings = ["Phillip K. Dick/'s Electric Dreams", "The Orville"]


for items in test_strings:
    if "/'s" in items:
        new_string = items.rsplit("/'s ", 1)[1]
        print(new_string)
