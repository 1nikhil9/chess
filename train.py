import agent1
from play import *
    
b = agent1.agent1()
b.BuildNetwork()
b.InitializeAndSave('./models/agent2/network.ckpt')
b.TrainNetwork('./models/agent2/network.ckpt')
