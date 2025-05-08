import asyncio

from datetime import datetime
from core.client_telnet import ClientTelnet
from core.olt import Olt

data_execucao = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def salvar_txt(items: list):
    with open(f"logs/onts_{data_execucao}.txt", "a", encoding="utf-8") as file:
        linha = " ".join(str(sub) for sub in items)
        file.write(linha + "\n")

async def main():
    cliente = ClientTelnet(
        host='10.55.160.2',
        usuario="smartolt",
        senha="rJXf2JA1p4NjTui"
    )
    
    olt = Olt(cliente=cliente)
    #onts = await olt.listar_onts(status="offline", gpon="0/10/13")
    onts = [
        
    ]
    
    print("="*100)
    print("\nLISTANDO ONTS\n")
    print("="*100)
    with open(f"logs/onts_{data_execucao}.txt", "a") as file:
        file.writelines("="*100 + "\n")
       
    for ont in onts:
        salvar_txt(ont)
        print(ont)
    
    print("="*100)
    print("\nREMOVENDO ONTS\n")
    print("="*100)
    for ont in onts:
       await olt.desprovisionar_ont(ont)
    
        
    print("="*100)
    print("\nADICIONANDO ONTS\n")
    print("="*100)
    for ont in onts:
        await olt.provisionar_ont(ont=ont, gpon_destino="0/2/7", vlan="1407")
  
if __name__ == "__main__":
    asyncio.run(main())
