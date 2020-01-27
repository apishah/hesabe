import httplib
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES


def pad(data):
    length = 32 - (len(data) % 32)
    data += chr(length)*length
    return data


def unpad(data):

    return data[0:-ord(data[-1])]


def encrypt(plainText, workingKey, iv):
    plainText = pad(str(plainText))
    enc_cipher = AES.new(workingKey.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    encryptedText = hexlify(enc_cipher.encrypt(plainText.encode('utf-8'))).decode('utf-8')
    return encryptedText


def decrypt(cipherText, workingKey, iv):
    encryptedText = unhexlify(cipherText)
    dec_cipher = AES.new(workingKey.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    decryptedText = unpad(dec_cipher.decrypt(encryptedText).decode('utf-8'))
    return decryptedText


def checkout(encencryptedText):
    conn = httplib.HTTPConnection("payment-api.eu-central-1.elasticbeanstalk.com")
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % encencryptedText
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'accesscode': "ab035967-3e92-4e07-9555-e7e4faf40a3f",
    }
    conn.request("POST", "/api/checkout", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
