import hashlib as hasher
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        seed = str(self.index) + \
                   str(self.timestamp) + \
                   str(self.data) + \
                   str(self.previous_hash)
        sha.update(seed.encode('utf-8'))
        return sha.hexdigest()

    def to_json(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @classmethod
    def create_genesis_block(cls):
        data = {
            "proof-of-work": 9,
            "transactions": None
        }
        return Block(
            0, date.datetime.now(),
            data,
            "0"
        )

    def next_block(self, data):
        next_index = self.index + 1
        next_timestamp = date.datetime.now()
        return Block(next_index, next_timestamp, data, self.hash)


if __name__ == '__main__':
    # Create the blockchain and add the genesis block
    blockchain = [Block.create_genesis_block()]
    previous_block = blockchain[0]

    num_of_blocks_to_add = 20

    for i in range(0, num_of_blocks_to_add):
        block_to_add = previous_block.next_block(f'hi {i}')
        blockchain.append(block_to_add)
        previous_block = block_to_add
        # Tell everyone about it!
        print("Block #{} has been added to the blockchain!".format(block_to_add.index))
        print("Hash: {}\n".format(block_to_add.hash))

    for e in blockchain:
        print(e.data, e.hash, e.previous_hash)
