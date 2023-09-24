# kript

Содержит такие функции как:

get_evm_native_balance(wallet_address, endpoints)
возвращает баланс нативных токенов у кошелька в виде словаря (адрес: баланс) 

get_erc20_of_wallet(wallet_address, contracts_erc20, provider)
возвращает баланс erc20 токенов у кошелька в виде словаря (название: баланс)

get_erc20_top(N, url)
парсит в data.json информацию об топ N erc20 токенах со сканера блокчейнов

