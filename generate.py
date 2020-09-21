import agent1
import time
from play import *

player = agent1.agent1()
player.BuildNetwork()

save_loc = './models/agent1/network.ckpt'

games = 0
maxMoves = 100000

t = [ time.time() ]
m = [ 0 ]
i = 0
while True:
    v, s = PlayMatch(games, player, save_loc, save_loc, False)
    games += 1
    
    if v >= maxMoves:
        break
    
    i += 1
    t.append(time.time())
    m.append(v)
    
    last = max(0, i-5)
    timeTaken = ((t[i] - t[last])*1.0)/(m[i] - m[last])
    rem = timeTaken*(maxMoves-v)
    
    print "Moves per second: ", 1.0/timeTaken
    print "Time remaining: ", rem
