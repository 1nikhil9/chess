import agent1
from play import *
import tensorflow as tf

player = agent1.agent1()
player.BuildNetwork()
a = './models/agent1/network.ckpt'
b = './models/agent2/network.ckpt'

games = 0
maxGames = 100

won = 0
drew = 0
lost = 0

won_white = 0
won_black = 0
drew_white = 0
drew_black = 0
lost_white = 0
lost_black = 0

while True:
    if games%2 == 0:
        s = PlayMatch(-1, player, b, a, False)
        if s > 0.75:
            won += 1
            won_white += 1
        elif s < 0.25:
            lost += 1
            lost_white += 1
        else:
            drew += 1
            drew_white += 1
    else:
        s = PlayMatch(-1, player, a, b, False)
        if s > 0.75:
            lost += 1
            lost_black += 1
        elif s < 0.25:
            won += 1
            won_black += 1
        else:
            drew += 1
            drew_black += 1
    
    games += 1
    total = won + lost + drew
    total_white = max(won_white + drew_white + lost_white, 1)
    total_black = max(won_black + drew_black + lost_black, 1)

    print "Won: ", won, (100.0*won)/total
    print "Drawn: ", drew, (100.0*drew)/total
    print "Lost: ", lost, (100.0*lost)/total
    print "Total: ", total
    
    print "Won (White): ", won_white, (100.0*won_white)/total_white
    print "Won (Black): ", won_black, (100.0*won_black)/total_black
    print "Drew (White): ", drew_white, (100.0*drew_white)/total_white
    print "Drew (Black): ", drew_black, (100.0*drew_black)/total_black
    print "Lost (White): ", lost_white, (100.0*lost_white)/total_white
    print "Lost (Black): ", lost_black, (100.0*lost_black)/total_black
