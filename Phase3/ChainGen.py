from Crypto.Hash import SHA3_256
import random



def MerkleTreeHash(block,TxCnt):


    tree = []

    #read the blocks , hashed then add to tree

    for i in range(0, TxCnt):
        bb = block[i * 9: (i * 9) + 9]
        str_2 = "".join(bb)
        str_3 = str_2.encode("UTF-8")
        hashh = SHA3_256.new(str_3)
        tree.append(hashh.digest())




    while (len(tree) > 1):
        tree2 = []
        for i in range(0, int(len(tree)/2)):
            Hash2 = (tree[2*i]) + (tree[(2*i)+1])
            hashed = SHA3_256.new(Hash2).digest()
            tree2.append(hashed)
        tree = tree2

    # tree[0] is the root

    return tree[0]


def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):
    TxLen=9

    if PrevBlock == '':
        Prev_pow = '00000000000000000000'

    else :
        Ppow = PrevBlock[len(PrevBlock)-2]
        Ppow = Ppow[14:len(Ppow)-1]
        hr = MerkleTreeHash(PrevBlock,TxCnt)
        pnonce = PrevBlock[len(PrevBlock)-1]
        pnonce = pnonce[7:len(pnonce)-1]
        pnonce = int(pnonce)
        result = hr + Ppow.encode('UTF-8') + pnonce.to_bytes((pnonce.bit_length()+7)//8, byteorder = 'big')
        Prev_pow = SHA3_256.new(result).hexdigest()




    H_r = MerkleTreeHash(block_candidate,TxCnt)

    Prev_pow_bit = Prev_pow.encode('UTF-8')
    while True:
        nonce = random.getrandbits(128)

        digest = H_r + Prev_pow_bit + nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')
        PoW = SHA3_256.new(digest).hexdigest()
        if PoW[0:PoWLen] == "0" * PoWLen:
            break



    NewBlock = block_candidate

    msg1 = 'Previous PoW: ' + Prev_pow +'\n'
    NewBlock.append(msg1)
    msg2 = 'Nonce: '+ str(nonce) + '\n'

    NewBlock.append(msg2)


    NewBlock_str = ''
    for r in range(0, len(NewBlock)):
        NewBlock_str += NewBlock[r]

    return NewBlock_str,PoW