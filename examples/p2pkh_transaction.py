from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.keys import Address, PrivateKey

def main():
    # always remember to setup the network
    setup('testnet')

    # create transaction input from tx id of UTXO (contained 0.4 tBTC)
    txin = TxInput('fb48f4e23bf6ddf606714141ac78c3e921c8c0bebeb7c8abb2c799e9ff96ce6c', 0)

    # create transaction output using P2PKH scriptPubKey (locking script)
    addr = Address('n4bkvTyU1dVdzsrhWBqBw8fEMbHjJvtmJR')
    txout = TxOutput(0.1, ['OP_DUP', 'OP_HASH160', addr.to_hash160(),
                           'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    # create another output to get the change - remaining 0.01 is tx fees
    change_addr = Address('mmYNBho9BWQB2dSniP1NJvnPoj5EVWw89w')
    change_txout = TxOutput(0.29, ['OP_DUP', 'OP_HASH160',
                                   change_addr.to_hash160(),
                                   'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    # create transaction from inputs/outputs -- default locktime is used
    tx = Transaction([txin], [txout, change_txout])

    # print raw transaction
    print("\nRaw unsigned transaction:\n" + tx.serialize())

    # use the private key corresponding to the address that contains the
    # UTXO we are trying to spend to sign the input
    sk = PrivateKey('cRvyLwCPLU88jsyj94L7iJjQX5C2f8koG4G2gevN4BeSGcEvfKe9')

    # note that we pass the scriptPubkey as one of the inputs of sign_input
    # because it is used to replace the scriptSig of the UTXO we are trying to
    # spend when creating the transaction digest
    from_addr = Address('myPAE9HwPeKHh8FjKwBNBaHnemApo3dw6e')
    sig = sk.sign_input(tx, 0, ['OP_DUP', 'OP_HASH160',
                                from_addr.to_hash160(), 'OP_EQUALVERIFY',
                                'OP_CHECKSIG'])
    #print(sig)

    # get public key as hex
    pk = sk.get_public_key()
    pk = pk.to_hex()
    #print (pk)

    # set the scriptSig (unlocking script)
    txin.script_sig = [sig, pk]
    signed_tx = tx.serialize()

    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + signed_tx)


if __name__ == "__main__":
    main()
