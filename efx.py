import random
from itertools import product

for items in range(6,13):
	print(items)
	for players in range(3,items):
		ATTEMPTS = int(10 * 1000 / ((players / 3)**6))
		min_efx_count = items**players
		for attempt in range(int(ATTEMPTS/ (players**(items-6)))):
			if attempt % (int((ATTEMPTS / 100) / players**(items-6)) + 1) == 0:
				print(attempt)
			arrays = [[] for k in range(players)]
			#array2 = []
			#array3 = []
			for i in range(players):
				for j in range(items):
					arrays[i].append(random.random())

			efx_count = 0

			for comb in product([i for i in range(players)], repeat=items):
				cross_values = [[0 for i in range(players - 1)] for j in range(players)]
				own_values = [[] for i in range(players)]

				for elem in range(items):
					for i in range(players):
						if comb[elem] != i:
							if comb[elem] > i:
								cross_values[i][comb[elem] - 1] -= arrays[i][elem]
							elif comb[elem] < i:
								cross_values[i][comb[elem]] -= arrays[i][elem]
						else:
							own_values[i].append(-arrays[i][elem])

				final_own_values = [0 for i in range(players)]

				for i in range(players):
					for elem in own_values[i]:
						final_own_values[i] = min(sum(own_values[i]) - elem, final_own_values[i])

				locally_efx = True
				for i in range(players):
					for j in range(players):
						if j > i:
							if final_own_values[i] < cross_values[i][j - 1]:
								locally_efx = False
						elif j < i:
							if final_own_values[i] < cross_values[i][j]:
								locally_efx = False

				if locally_efx:
					efx_count += 1

			if efx_count == 0:
				print("EFX FULL FAILURE. ALERTING ALL SYSTEMS")
				import pdb
				pdb.set_trace()
			else:
				min_efx_count = min(efx_count, min_efx_count)
		print("items={}, players={}, min_efx_count={}".format(items, players, min_efx_count))
