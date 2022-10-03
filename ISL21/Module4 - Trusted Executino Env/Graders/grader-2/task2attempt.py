import os
import requests
import hashlib
import time 
import binascii 
admin = "admin$00000000001636647758884$003575c066c711913e0b95b65aa1a9810c4726af722fc9a27974845a36ffb5aa4011111111111111111111111111111111af4a445d5bfee31c1fba656aefb089f112117264ee42ae55001f1d1a3bc561787439810809ab69fa140077db71232044813b626b53623b6d1a2fbc22f65f12eadfb7a4bc563719c11e063b744f5f91f9c412272ce5af58fbeace9d7862a3c1de8cbb695293a6fe76bf77e9493ad8eab1"

hello = "hello$00000000001636647758889$000389289a839f8104a19535a57c60be21c2da9312df51308e0cd363ba82885b51111111111111111111111111111111112880ccda64f655478e053e178a2b4caf3441570c37c51e5eddeb4fd3f5a15d94653de7101e9c59229b666124029fc7d2dbf080223cc1e27635e9ea1f374e44bf86208d23fe97661d97ed63d5b1585afed679e7d2855f55d403e71c50ebe0390207d926be16293d3d2aa55e6ea6d9f013"

get = "gets$000000000001636647759292$0011434d9f6277a8dcf01ba29124a24c7fcad984da0feb3190ed8b19fced10385a111111111111111111111111111111112880ccda64f655478e053e178a2b4cafbb53d6f4e3d6208f387806d7fdd1b29d1ef0d44c78d3f67d087385cc23e857792c42ab947b9925bb962c44ce19571c245cedc1efaf00e4e745773ec52a8de4baaa3ea5f7b11113987c0c8283a400c30e9cc7e30a72efae130bb7369a9e391735"
store1 = "store$00000000001636647759693$0016fd8ebd2e696dc2323d83ce491aafa0d63f74a40ea31f924159d041837955a2111111111111111111111111111111112880ccda64f655478e053e178a2b4cafda230f5afde3a2b3e0b8b1fab8932fb5f92247f1a61e1ff48c154a7d889c8a90230a7c1edede1ef3db4d4614116d152ba252906ad668420f46e3321f294cc29272e39c5d99004d5cd4fd63b148c87970f5ae3ddce9d30afa66298b53b414b316"
store2 = "store$00000000001636647764914$002878b97f22115c59fbb3fb4b41564a6da24ecc24c48796195c1e42d5d0e5c7ae111111111111111111111111111111112880ccda64f655478e053e178a2b4cafda230f5afde3a2b3e0b8b1fab8932fb5a31a8733254af8eb083fd31fe7a10c364799ac5800ba50b75b32e01b2766953658320f6d1e4d99487824ae501104f85ce6a467afd899cdea1a7d091a1572e0d7f8e9c7906ba8fa066517fa3c167dce4f"

admintwo = "admin$00000000001636647770167$00023e67314ec1ac80c7df2ee1f2c5cecb019df64c3362d198236aa68d363a10c911111111111111111111111111111111af4a445d5bfee31c1fba656aefb089f1fcd61d26f3a5c0b85aa902e80032ad7e2e09ce67e206d707c137917710832db26a7fff8c6a7831bac40ed60042e138b8d32eff104960fa9af312358ecad3c257903337a3ba1940030464248eb9677bc7e2d594a5495199ca52923101fc8da202"


url = "http://127.0.0.1:37200"
def parse(msg):
    type = msg[:16]
    time = msg[16:32]
    mac = msg[32:96]
    body = msg[96:96+256]
    iv = body[:32]
    enc_msg = body[32:]
    return type, time, mac, iv, enc_msg    


def setup():
   os.system("/home/isl/t2/run.sh > /dev/null")
   #os.system("pkill -9 node")
   #os.system("node --no-warnings /home/isl/t2/peripheral &")

def firstthreeflags():
    requests.post(url+"/store",store1)
    requests.post(url+"/store",store2) #Get flag 2.2
    requests.post(url+"/hello",hello) #2.3
    requests.post(url+"/store",store2) #2.1
    requests.post(url+"/store",store2) #2.1
    requests.post(url+"/store",store2) #2.1
    time.sleep(1)

def lastone():
    type,msg_time,mac,iv,enc_msg = parse(admin)
    splitM(admin)
    time.sleep(1)
    ptxt = '<start_cmd><mes cd="init"></mes></start_cmd>' 
    try_command("init",iv,enc_msg,type,msg_time,ptxt)

def splitM(m):
    contt = m[:16]
    ts = m[16:2*16]
    print(f"content type: {contt}")
    print(f"timestamp: {ts}")
    mac = m[2*16:2*16+64]
    print(f"MAC: {mac}")
    hexenc = m[2*16+64:2*16+64+256]
    assert len(hexenc) == 256
    #print(f"AES CBC len: {len(hexenc)}")
    iv = hexenc[:32]
    hexenc = hexenc[32:]
    print(f"IV: {iv}")
    print(f"hexenc without IV: {hexenc}\n")
                
def try_command(command,iv,enc_msg,type,timeee,ptxt):
    command = "<start_cmd><mes cd=\""+command+"\"></mes></start_cmd>"
  #  command = binascii.hexlify(command).decode()

 #   print(command)
 #   print(iv)
    iv = "1"*32
    xor = ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(iv,ptxt)])
    new_iv = ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(command,xor)])
    print(new_iv)
  #  iv = b'1'*32
  #  print(iv)
  #  new_iv = hex(int(iv,16) ^ int(iv,16))[2:] #  bytes([a ^ b for a,b in zip(ptxt,iv)])
  #  new_iv_temp =  hex(int(iv,16) ^ int(new_iv,16))[2:]  # bytes([a ^ b for a,b in zip(command,new_iv)])
  #  new_iv = binascii.unhexlify(new_iv_temp).decode('utf-8')
  #  print(new_iv_temp)
  #  print(bytearray.fromhex(new_iv_temp)	)
    #print(new_iv)
    enc_body = new_iv + enc_msg
    mac_value = binascii.unhexlify(new_iv) + binascii.unhexlify(enc_msg.encode('utf-8'))
    print(mac_value)
    #    print(binascii.unhexlify(enc_body))
    mac = (hashlib.sha256(mac_value).hexdigest())
    enc_body = new_iv + enc_msg
    pkt = type + str(int(time.time()*1000))+"$00" + mac + enc_body
    splitM(pkt)

lastone()
