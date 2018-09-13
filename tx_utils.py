def calc_sum_of_tx(tx_sum, tx_amount):
    if tx_amount:
        return tx_sum + sum(tx_amount)
    return tx_sum
