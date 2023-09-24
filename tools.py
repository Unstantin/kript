import web3
from web3 import Web3
import requests
import json
import time
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

contracts_erc20 = [
    '0x6b175474e89094c44da98b954eedeac495271d0f', #dai
    '0xdac17f958d2ee523a2206206994597c13d831ec7', #usdt
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', #usdc
    '0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce'  #shib
]

ABI = '[{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"initSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

def get_evm_balance(wallet_address):
    checksum_address = Web3.to_checksum_address(wallet_address)

    endpoints = [
        'https://rpc.ankr.com/polygon',
        'https://rpc.ankr.com/eth',
        'https://rpc.ankr.com/bsc',
        'https://rpc.ankr.com/fantom',
        'https://rpc.ankr.com/avalanche',
        'https://rpc.ankr.com/optimism',
        'https://rpc.ankr.com/gnosis',
        'https://rpc.ankr.com/celo',
        'https://rpc.ankr.com/mantle',
        'https://rpc.ankr.com/harmony'
    ]

    for p in endpoints:
        web3 = Web3(Web3.HTTPProvider(p))
        balance = web3.eth.get_balance(checksum_address)
        name = p[-p[::-1].find('/'):]
        print(f'{name:10} {balance}')

def get_erc20_of_wallet(wallet_address):
    for address_erc20 in contracts_erc20:
        web3 = Web3(Web3.HTTPProvider('https://ethereum.blockpi.network/v1/rpc/public'))

        checksum_erc20 = web3.to_checksum_address(address_erc20)
        contract = web3.eth.contract(address=checksum_erc20, abi=ABI)

        checksum_wallet = web3.to_checksum_address(wallet_address)
        balance = contract.functions.balanceOf(checksum_wallet).call()
        balance_humanity = web3.from_wei(balance, 'ether')
        print(balance_humanity)

def get_erc20_top(N):
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get('https://etherscan.io/tokens')
    driver.find_element(By.XPATH, '//*[@id="btnCookie"]').click()

    res = []
    for i in tqdm(range(1, N + 1)):
        index = i % 51 + i // 51
        try:
            driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_tblErc20Tokens"]/table/tbody/tr[{index}]/td[2]/a').click()
        except:
            iframe = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_tblErc20Tokens"]/table/tbody/tr[{index}]')
            ActionChains(driver).scroll_to_element(iframe).perform()
            time.sleep(2)

            driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_tblErc20Tokens"]/table/tbody/tr[{index}]/td[2]/a').click()

        address = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_divSummary"]/div[2]/div[3]/div/div/div[1]/div/a[1]').text
        name = driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div/div[1]/div/span').text
        name = name[:name.find(' (')]
        tiсket = driver.find_element(By.XPATH, '//*[@id="content"]/section[1]/div/div[1]/div/span/span').text[1:-1]
        url = driver.current_url

        data = {
            "address": address,
            "name": name,
            "ticket": tiсket,
            "url": url
        }
        res.append(data)

        driver.back()

        if i % 50 == 0:
            xpath_but = '//*[@id="ContentPlaceHolder1_divPagination"]/nav/ul/li[4]/a'
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.find_element(By.XPATH, xpath_but).click()
            time.sleep(5)

    with open("data.json", "w") as f:
        json.dump(res, f)

test_wallet_address = '0x7bfee91193d9df2ac0bfe90191d40f23c773c060'

#get_erc20_of_wallet(test_wallet_address)
#get_erc20_top(100)

# with open("data.json", "r") as f:
#      data = json.load(f)

#print(data[0]["name"])













