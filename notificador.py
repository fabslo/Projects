import requests
import hashlib
from bs4 import BeautifulSoup
import difflib
import time
from telegram import Bot

# Dados do Telegram
TELEGRAM_TOKEN = '7316687860:AAHbGMTjyJ2tC6w3Rr9S8ofPGpFNuvBhLNE'
CHAT_ID = '-4276666045'

# URL do site que você deseja monitorar
url = 'https://sorteiosbuq.com.br/acoes/2y91parwa6'
content_hash = ''
old_content = ''

# Inicializa o bot do Telegram
bot = Bot(token=TELEGRAM_TOKEN)

# Função para obter o conteúdo do site e extrair partes relevantes
def get_site_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Identifique e extraia as partes relevantes do HTML
    # Supondo que queremos extrair o horário de uma tag específica
    # Aqui você deve ajustar a extração para suas necessidades específicas
    relevant_content = soup.find('div', {'class': 'grid gap-4 grid-cols-1 md:grid-cols-3 my-4 lg:grid-cols-5 px-4'}).get_text(separator='\n', strip=True)
    
    return relevant_content

# Função para calcular o hash do conteúdo
def hash_content(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# Função para enviar uma mensagem via Telegram
def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

while True:
    new_content = get_site_content(url)
    new_hash = hash_content(new_content)
    
    if new_hash != content_hash:
        send_telegram_message("Um título foi encontrado!")
        
        if old_content:
            diff = difflib.unified_diff(old_content.splitlines(), new_content.splitlines(), lineterm='')
            diff_message = '\n'.join(diff)
            send_telegram_message(f"Diferença encontrada:\n{diff_message}")
        
        # Atualize os valores para a próxima verificação
        content_hash = new_hash
        old_content = new_content
    
    # Aguarde 60 segundos antes de verificar novamente
    time.sleep(60)
