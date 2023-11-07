from classes.device import Device

node=Device("localhost", 8888,"listener")
try:
    node.listen()
except KeyboardInterrupt:
    print("We have finished this method")
    
for dataElement in node.dataStorage:
    print(str(dataElement))
