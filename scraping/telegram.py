
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio
from dotenv import load_dotenv
import os
import sys
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import my_functions as mf

load_dotenv()

API_ID = os.getenv("API_ID_TELEGRAM")
API_HASH = os.getenv("API_HASH_TELEGRAM")

inicio = datetime(2025, 11, 17, tzinfo=timezone.utc)
final  = datetime(2025, 11, 27, tzinfo=timezone.utc)

async def qvapay():
    async with TelegramClient("datapyme", API_ID  ,API_HASH) as client:
        async for m in client.iter_messages("qvapay_p2p",  offset_date=final):
               mf.parser_qvapay(id=str(m.id), date=str(m.date), text=str(m.text), file=r"..\\data\\qvapay.json")
               print(m.date)
               await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(qvapay())
  
        
# 🟢 #Compra $100 por $100.00 en #CLASICA

# 🤑 Peer: #juanantonioiglesiasrosa
# 📉 Ratio: $1.00 x USD
# ✨ Rating: 4.97 ⭐️
# 🔁 Operaciones: 1613
# ⏱️ Miembro desde hace 1 año

# KYC 🪪 VIP 🚫 GOLD 👑



# Llamar o SMS 53591670 📲♨️ sino estoy en línea

# ---------------------------------------

# 🔴 #Venta $20 por $10000.00 en #CUP

# 🤑 Peer: #yamismeidydiaz
# 📉 Ratio: $500.00 x USD
# ✨ Rating: 4.96 ⭐️
# 🔁 Operaciones: 224
# ⏱️ Miembro desde hace 4 años

# KYC 🪪 VIP 🚫 GOLD 🚫
