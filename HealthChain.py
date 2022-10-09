from hashlib import sha256
from json import dumps
from os import stat
from datetime import date
from RSA_Implementation import get_keys, new_signature, verify_signature

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(
            self,
            unconfirmed_data={},
            chain=[Block(0, {"hash": "0", "size": 0, "date": "0000-00-00"}, "0")]
    ):
        self.unconfirmed_data = unconfirmed_data
        self.chain = chain

    def copy(self):
        return Blockchain(self.unconfirmed_data, self.chain)

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        if (self.chain[-1].hash == block.previous_hash and  # if prev. hash tallies with last hash on blockchain
            proof.startswith('0' * Blockchain.difficulty) and  # and the newest hash is in the correct format
            proof == block.compute_hash()  # and the hash shown tallies with the block itself
        ):
            block.hash = proof  # it is now the official hash
            self.chain.append(block)  # and the block goes on the blockchain

    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_new_entry(self, path, auth):
        with open(path, 'rb') as f:
            fb = f.read()
            file_hash = sha256(fb).hexdigest()
        file_size = stat(path).st_size
        file_date = str(date.today())
        entry = {"hash": file_hash, "size": file_size, "date": file_date, "auth": auth}
        self.unconfirmed_data = entry

    def mine(self):
        """
        This function serves as an interface to add the pending
        data to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_data:
            return False
        file_hash = self.unconfirmed_data["hash"]
        signature, public_key = self.unconfirmed_data["auth"]
        if public_key not in key_registry:
            return False
        if not verify_signature(signature, public_key, file_hash):
            return False

        last_block = self.chain[-1]

        new_block = Block(index=last_block.index + 1,
                          data=self.unconfirmed_data,
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_data = []
        return new_block.index

    def validate(self, path, record_date):
        with open(path, 'rb') as f:
            fb = f.read()
            file_hash = sha256(fb).hexdigest()
        for blocks in self.chain:
            if (blocks.data["hash"] == file_hash and
                blocks.data["size"] == stat(path).st_size and
                blocks.data["date"] == record_date
            ):
                return True

    def get(self):
        returnstring = ""
        for blocks in self.chain:
            # print(blocks.data)  utility function for debugging
            returnstring += str(blocks.data)
        return returnstring

    def push_to_peers(self):
        pass


class Peer:
    def __init__(self):
        self.chain = Blockchain()

    def receive_entry(self, blockchain):
        if blockchain.get() == self.chain.get():
            blockchain.push_to_peers()
            self.chain = blockchain.copy()
            self.chain.mine()
            print("Entry Received")
            return blockchain.copy()
        else:
            print("Entry Error")


class Doctor:
    def __init__(self):
        self.chain = Blockchain()
        public_key, private_keys = get_keys()
        self.public_key = public_key
        self.private_keys = private_keys
        key_registry.append(public_key)
        print("New doctor: ", public_key)

    def receive_entry(self, blockchain):
        if blockchain.get() == self.chain.get():
            blockchain.push_to_peers()
            self.chain = blockchain
            self.chain.mine()
            print("Entry Received")
            return self.chain.get()
        else:
            print("Entry Error")

    def add_to_chain(self, path):
        with open(path, 'rb') as f:
            fb = f.read()
            file_hash = sha256(fb).hexdigest()
        file_size = stat(path).st_size
        file_date = str(date.today())
        auth = new_signature(self.public_key, self.private_keys, file_hash), self.public_key
        entry = {"hash": file_hash, "size": file_size, "date": file_date, "auth": auth}
        self.chain.unconfirmed_data = entry
        self.chain.push_to_peers()
        print("Added to chain")
        return self.chain

    def validate(self, path, record_date):
        with open(path, 'rb') as f:
            fb = f.read()
            file_hash = sha256(fb).hexdigest()
        for blocks in self.chain.chain:
            if (blocks.data["hash"] == file_hash and
                blocks.data["size"] == stat(path).st_size and
                blocks.data["date"] == record_date
            ):
                return True
        else:
            return False

key_registry = []