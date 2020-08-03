import os
import sys

def str_dec(str):
  key = os.environ['DEC_KEY']
  klen = len(key)
  res = ""
  for i in range(len(str)):
    c = ord(str[i])
    k = ord(key[i % klen])
    res += chr(c ^ k)
  return res

def Telegram_API_Key():
  return str_dec(bytes.fromhex("537f7c6a7d59637f757f7e043509272a0b3f350b050a1e021122303c70742f363d332b130a122b163d17210d511b").decode('utf-8'))
