import node
from node import Node
node = Node("127.0.0.1", 8080, 1)

# Generate the keys
publickey, privatekey = node.create_keys()

# Encrypt a message
message = "Hello, world!"

ciphertext = node.encrypt(message, f"public_key{node.id}.pem")

# Decrypt the message
plaintext = node.decrypt(ciphertext, f"private_key{node.id}.pem")

print(plaintext)