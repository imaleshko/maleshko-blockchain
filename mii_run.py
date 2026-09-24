import json

from mii_blockchain import MIIBlockchain


def mii_run():
    blockchain = MIIBlockchain()

    while True:
        print("1 - провести транзакцію")
        print('2 - переглянути мемпул')
        print('3 - переглянути останній блок')
        print('4 - переглянути всі блоки')
        print('5 - вийти')

        mii_choice = input("Введіть номер опції: ")

        match mii_choice:
            case '1':
                try:
                    sender = input("Введіть адресу відправника: ")
                    recipient = input("Введіть адресу отримувача: ")
                    amount = float(input("Введіть суму: "))
                except ValueError:
                    print("Сума повинна бути числом")
                    continue
                blockchain.mii_new_transaction(sender, recipient, amount)
                print("Транзакція успішно проведена")

                if blockchain.mii_current_transactions_len >= 2:
                    blockchain.mii_new_block(blockchain.mii_last_block_hash,
                                             blockchain.mii_proof_of_work(blockchain.mii_last_block_proof))
                    print("Згенеровано новий блок")
            case '2':
                current_transaction = blockchain.mii_current_transactions
                if not current_transaction:
                    print("Мемпул порожній")
                else:
                    print(json.dumps(blockchain.mii_current_transactions, indent=4))
            case '3':
                print(json.dumps(blockchain.mii_last_block, indent=4))
            case '4':
                print(json.dumps(blockchain.mii_chain, indent=4))
            case '5':
                break
            case _:
                print("Виберіть опцію")


mii_run()
