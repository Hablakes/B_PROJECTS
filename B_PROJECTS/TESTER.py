from .BX_CRYPT_TESTING_0 import *


def test():
    message = [ord(x) for x in "TEST MESSSAGE for testing!"]

    key = "!!#jdsafklajdslk;fjads;klfj###"

    cipher_text = encrypt_function(key, message)

    decrypted_text = decrypt(key, cipher_text)

    assert decrypted_text == message
