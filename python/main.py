import contract_info as cf
# Импорт модуля с информацией о контракте, такой как адрес и ABI

from web3 import Web3
# Импорт класса Web3 для взаимодействия с Ethereum

from web3.middleware import geth_poa_middleware
# Импорт промежуточного ПО для работы с Geth POA (Proof of Authority)

# Создание экземпляра Web3 для подключения к Ethereum узлу
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Внедрение промежуточного ПО для корректной работы с Geth, использующим POA
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Создание объекта контракта с использованием адреса и ABI из импортированного модуля
contract = w3.eth.contract(address=cf.CONTRACT_ADDRESS, abi=cf.ABI)
# Получение списка аккаунтов, доступных в узле Ethereum
accounts = w3.eth.accounts

def register():
    password = input("Введите пароль: ")  # Запрос пароля у пользователя

    # Инициализация переменных для проверки критериев пароля
    uppercase = False
    lowercase = False
    digit = False
    special = False

    # Проверка каждого символа в пароле
    for char in password:
        if char.isupper():  # Проверка на наличие заглавной буквы
            uppercase = True
        elif char.islower():  # Проверка на наличие строчной буквы
            lowercase = True
        elif char.isdigit():  # Проверка на наличие цифры
            digit = True
        elif char in "!@#$%^&*()":  # Проверка на наличие специального символа
            special = True

    # Проверка соответствия пароля всем критериям безопасности
    if len(password) >= 12 and uppercase and lowercase and digit and special and "password123" not in password and "qwerty123" not in password:
        account = w3.geth.personal.new_account(password)  # Создание нового аккаунта в Geth
        print("Вы успешно зарегестрированы.")
        print(f"Ваш публичный ключ: {account}")
    else:
        print("Пароль должен быть не менее 12 символов, а так же содержать цифры, специальные симолы, строчные и заглавные буквы!")


def login():
    public_key = input("Введите ваш публичный ключ: ")
    password = input("Введите пароль: ")
    try:
        w3.geth.personal.unlock_account(public_key, password)
        print("Авторизация прошла успешно!")
        return public_key
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return None

def get_balance(account):
    public_key = input("Введите ваш публичный ключ чтобы узнать свой баланс на смарт контракте: ")
    try:
        balance = contract.functions.getBalanceUSER(public_key).call({
            'from': account
        })
        print(f"Ваш баланс на смарт-контракте: {balance}")
    except Exception as e:
        print(f"Ошибка получения баланса: {e}")

def withdraw(account):
    try:
        value = int(input("Введите кол-во WEI для отправки на счёт: "))
        tx_hash = contract.functions.withDraw().transact({
            'from' : account,
            'value': value
        })
        print(f"Ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки WEI: {e}")

def deposit(account):
    try:
        value = int(input("Введите кол-во WEI для пополнения смарт-контракта: "))
        tx_hash = contract.functions.deposit().transact({
            'from' : account,
            'value': value
        })
        print(f"Ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки WEI: {e}")

def createEstate(account):
    try:
        estateAddress = input("Введите адрес: ")
        size = int(input("Введите площадь: "))
        esType = int(input("Введите номер типа: "))

        tx_hash = contract.functions.createEstate(size, estateAddress, esType).transact({
            'from' : account,
        })
        print(f"Вы успешно создали недвижимость. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def statusEstate(account):
    try:
        id = int(input("Введите id недвижимости: "))

        tx_hash = contract.functions.statusEstate(id).transact({
            'from' : account,
        })
        print(f"Вы изменили статус недвижимости. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка изменения статуса недвижимости: {e}")

def createAd(account):
    try:
        idEstate = int(input("Введите id недвижимости: "))
        price = int(input("Введите цену: "))

        tx_hash = contract.functions.createAd(price, idEstate).transact({
            'from' : account,
        })
        print(f"Вы создали объявление. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def statusAD(account):
    try:
        id = int(input("Введите id объявления: "))

        tx_hash = contract.functions.statusAd(id).transact({
            'from' : account,
        })
        print(f"Вы изменили статус объявления. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка изменения статуса объявления: {e}")

def buyEstate(account):
    try:
        idAd = int(input("Введите id объявления о недвижимости: "))
        buyerId = input("Введите публичный ключ покупателя: ")

        tx_hash = contract.functions.buyEstate(idAd,buyerId).transact({
            'from' : account,
        })
        print(f"Вы купили недвижимость. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка покупки недвижимости: {e}")

def balance(account):
    try:
        value = int(input("Введите количество Ether: "))
        if not value:
            return
        if value <= 0:
            print("Значение должно быть больше нуля")
            return
        tx_hash = w3.eth.send_transaction({
            'from': w3.eth.coinbase,
            'to': account,
            'value': value * 1000000000000000000
        })
        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка пополнения баланса: {e}")

def main():
    account = ""
    while True:
        if account =="" or account == None:
            choice = input("""Добро пожаловать в систему смарт-контрактов!
            \nЧтобы начать работу войдите или зарегестрируйтесь :)
            \n1. Регистрация
            \n2. Авторизация
            \n3. Выйти из аккаунта
            \n4. Выйти из программы
            \nВведите ваш выбор: """)
            match choice:
                case "1":
                    register()
                case "2":
                    account = login()
                case "3":
                    account = ""
                case "4":
                    return False
                case _:
                    print("Некорректный ввод")
        else:
            choice = input("""Список действий со смарт-контраком:
            \n1. Просмотр информации
            \n2. Недвижимость
            \n3. Объявления
            \n4. Работа с балансом
            \n5. Выйти
            \nВведите ваш выбор: """)
            match choice:
                case "1":
                    choice = input("""Список:
                    \n1. Доступная недвижимость
                    \n2. Открытые объявления
                    \n3. Баланс аккаунта]
                    \n4. Баланс смарт-контракта
                    \n5. Выйти
                    \nВведите ваш выбор: """)
                    match choice:
                        case "1":
                            try:
                                estates = contract.functions.getEstate().call({'from': account})
                                if not estates:
                                    print("Нет недвижимостей для отображения")
                                else:
                                    for i in range(len(estates)):
                                        print(estates[i])
                            except Exception as e:
                                print(f"Произошла ошибка: {e}")
                        case "2":
                            try:
                                ads = contract.functions.getAds().call({'from': account})
                                if not ads:
                                    print("Нет объявлений для отображения")
                                else:
                                    for ad in ads:
                                        print(ad)
                            except Exception as e:
                                print(f"Произошла ошибка: {e}")
                        case "3":
                            print(f"Баланс аккаунта: {w3.eth.get_balance(account)/1000000000000000000} ETH")
                        case "4":
                            get_balance(account)
                        case "5":
                            continue
                        case _:
                            print("Выберите от 1 до 5")
                case "2":
                    choice = input("""Список действий с недвижимостью:
                    \n1. Создать недвижимость
                    \n2. Изменить статус недвижимости
                    \n3. Купить недвижимость
                    \n4. Выйти
                    \nВведите ваш выбор: """)
                    match choice:
                        case "1":
                            createEstate(account)
                        case "2":
                            statusEstate(account)
                        case "3":
                            buyEstate(account)
                        case "4":
                            continue
                        case _:
                            print("Выберите от 1 до 4")
                case "3":
                    choice = input("""Список действий с объявлениями:
                    \n1. Создать объявление
                    \n2. Изменить статус объявления
                    \n3. Выйти
                    \nВведите ваш выбор: """)
                    match choice:
                        case "1":
                            createAd(account)
                        case "2":
                            statusAD(account)
                        case "3":
                            continue
                        case _:
                            print("Выберите от 1 до 3")
                case "4":
                    choice = input("""Список действий со средствами:
                    \n1. Вывести средства с контракта
                    \n2. Пополнить баланс контракта
                    \n3. Пополнить баланс пользователя
                    \n4. Выйти\nВведите ваш выбор: """)
                    match choice:
                        case "1":
                            withdraw(account)
                        case "2":
                            deposit(account)
                        case "3":
                            balance(account)
                        case "4":
                            continue
                        case _:
                            print("Выберите от 1 до 4")
                case "5":
                    account = ""
                case _:
                    print("Выберите от 1 до 5")

if __name__ == "__main__":
    main()
