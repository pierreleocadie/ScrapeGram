"""
CODE OWNER : https://github.com/lorenzodifuccia
LINK OF THE ORIGINAL GITHUB GIST : https://gist.github.com/lorenzodifuccia/c857afa47ede66db852e6a25c0a1a027
"""
import base64
import struct
import datetime
import binascii

from urllib.parse import quote_plus

# pip install pycryptodomex
from Cryptodome import Random
from Cryptodome.Cipher import AES

# pip install PyNaCl
from nacl.public import PublicKey, SealedBox

def encrypt_password(key_id, pub_key, password, version=10):
    key = Random.get_random_bytes(32)
    iv = bytes([0] * 12)

    time = int(datetime.datetime.now().timestamp())

    aes = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16)
    aes.update(str(time).encode('utf-8'))
    encrypted_password, cipher_tag = aes.encrypt_and_digest(password.encode('utf-8'))

    pub_key_bytes = binascii.unhexlify(pub_key)
    seal_box = SealedBox(PublicKey(pub_key_bytes))
    encrypted_key = seal_box.encrypt(key)

    encrypted = bytes([1,
                       key_id,
                       *list(struct.pack('<h', len(encrypted_key))),
                       *list(encrypted_key),
                       *list(cipher_tag),
                       *list(encrypted_password)])
    encrypted = base64.b64encode(encrypted).decode('utf-8')

    return f'#PWD_INSTAGRAM_BROWSER:{version}:{time}:{encrypted}'
    #return quote_plus(f'#PWD_INSTAGRAM_BROWSER:{version}:{time}:{encrypted}')


if __name__ == "__main__":
    print(encrypt_password(28, "25dde515c83a355c067df0cc17beb7a60023c8743ab94938c4f90c053a926b31", "CHANGE_PASSWORD_HERE"))