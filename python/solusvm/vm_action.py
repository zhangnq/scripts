#coding:utf-8

from solusvm import SolusVMClient
from config import SOLUS_URL,SOLUS_CLIENTS

for solus_client in SOLUS_CLIENTS:
    solus_client = SolusVMClient(SOLUS_URL,solus_client["key"],solus_client["hash"])
    
    print solus_client.serverStatus().text
