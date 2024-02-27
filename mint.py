from web3 import Web3
import json
import sys
import time
import os
import random

#Установи ГАЗович!!!! 89 строка
#Скрипт активирует функцию mint, контракта ZerionDna, фриминт в сети ETH.  
#Отправляет транзы почередно с рандомной заданной задержкой. Проверяет газ каждые 10сек и отправляет когда падает до заданных пределов
#для его работы создаем файлы mint.txt (для приватников), last_successful_tx6.txt (для записи посл.транзакции - чтобы после остановки скрипта всегда можно было увидеть посл.успешную транзу)



# Настройки
eth_rpc_url = 'https://eth.meowrpc.com'
contract_address = 'paste your CA'
private_keys_file_path = 'mint.txt'
web3 = Web3(Web3.HTTPProvider(eth_rpc_url))
assert web3.isConnected(), "Не удалось подключиться к Ethereum RPC"
contract_address = web3.toChecksumAddress(contract_address)

# Загрузка приватных ключей
private_keys = []
with open(private_keys_file_path, 'r') as file:
    private_keys = [line.strip() for line in file]

# ABI контракта (замените на актуальный ABI вашего контракта)
contract_abi = json.loads('[.....]
# Создание объекта контракта
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Файл для сохранения информации о последней успешной транзакции
last_tx_file = 'last_successful_tx6.txt'

# Функция для чтения последней успешной транзакции из файла
def read_last_successful_tx():
    if os.path.exists(last_tx_file):
        with open(last_tx_file, 'r') as file:
            return file.read()
    return None


# Функция для сохранения последней успешной транзакции в файл
def save_last_successful_tx(tx_info):
    with open(last_tx_file, 'w') as file:
        file.write(tx_info)

#читаем информацию о последней успешной транзакции
last_successful_tx = read_last_successful_tx()

# Функция отправки транзакций
def send_transactions(private_keys, contract, target_gas_price_gwei):
    for private_key in private_keys:
        account = web3.eth.account.privateKeyToAccount(private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        
        # Ожидание подходящей стоимости газа
        while True:
            current_gas_price = web3.eth.gasPrice
            if current_gas_price <= web3.toWei(target_gas_price_gwei, 'gwei'):
                break
            print(f"Текущая стоимость газа {Web3.fromWei(current_gas_price, 'gwei')} gwei выше цели {target_gas_price_gwei} gwei.")
            time.sleep(10)
        
        tx = {
            'type': '0x2',
            'chainId': web3.eth.chainId,
            'gas': 115849,
            'maxPriorityFeePerGas': web3.toWei(0.1, 'gwei'),
            'maxFeePerGas': web3.toWei(target_gas_price_gwei, 'gwei'),
            'nonce': nonce,
            'to': contract_address,
            'value': 0,
            'data': '0x1249c58b72db8c0b',
        }
        
        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        print(f'\033[92m>>> Успешно | Адрес: {account.address} | Хеш: {tx_hash.hex()} | Стоимость газа: {Web3.fromWei(desired_gas_price, "gwei")} gwei\033[0m')
        save_last_successful_tx(f'Адрес: {account.address} | Хеш: {tx_hash.hex()}')
        
        time.sleep(random.randint(3, 5))

try:
    send_transactions(private_keys, contract, 18)
except KeyboardInterrupt:
    print('\033[92m>>>Скрипт остановлен пользователем.\033[0m')
    with open('last_successful_tx6.txt', 'r') as file:
        last_tx = file.read()
    print('\033[92mПоследняя успешная транзакция: {}\033[0m'.format(last_tx))
