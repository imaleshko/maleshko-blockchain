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
                sender = input("Введіть адресу відправника: ")
                recipient = input("Введіть адресу отримувача: ")
                amount = float(input("Введіть суму: "))
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
                    print(blockchain.mii_current_transactions)
            case '3':
                print(blockchain.mii_last_block)
            case '4':
                print(blockchain.mii_chain)
            case '5':
                break
            case _:
                print("Виберіть опцію")


mii_run()
