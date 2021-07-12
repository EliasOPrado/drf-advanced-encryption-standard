import
base64, re
from Crypto.Cipher import AES
from Crypto import Random
from django.conf import settings


class AESCipher:
    """
      Usage:
      aes = AESCipher( settings.SECRET_KEY[:16], 32)
      encryp_msg = aes.encrypt( 'The Hyper Secret Message Here.' )
      msg = aes.decrypt( encryp_msg )
      print("'{}'".format(msg))
    """

    def __init__(self, key, blk_sz):
        self.key = key
        self.blk_sz = blk_sz

    def encrypt(self, raw):
        # raw is the main value
        if raw is None or len(raw) == 0:
            raise NameError("No value given to encrypt")
        raw = raw + '\0' * (self.blk_sz - len(raw) % self.blk_sz)
        raw = raw.encode('utf-8')
        # Initialization vector to avoid same encrypt for same strings.
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        # enc is the encrypted value
        if enc is None or len(enc) == 0:
            raise NameError("No value given to decrypt")
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, iv)
        return re.sub(b'\x00*$', b'', cipher.decrypt(enc[16:])).decode('utf-8')


