import sys

games_played = 0
scores = {}
won = {}

for A, scoreA, B, scoreB in map(lambda line: line.split(), sys.stdin):
    if A not in scores:
        scores[A] = 0
        won[A] = 0
    if B not in scores:
        scores[B] = 0
        won[B] = 0
    scoreA, scoreB = int(scoreA), int(scoreB)

    scores[A] += scoreA
    scores[B] += scoreB
    games_played += 1
    if scoreA > scoreB:
        print("%s wins with score %d" % (A, scoreA))
        won[A] += 1
    elif scoreB > scoreA:
        print("%s wins with score %d" %(B, scoreB))
        won[B] += 1
    else:
        won["DRAW"] += 1

print("Data from %d played games: overall victor is %s" % (games_played, max(won.iteritems())[0]))
for player, victories in won.iteritems():
    print("\tPlayer %s won %d games, total score %d." %(player, victories, scores[player]))

