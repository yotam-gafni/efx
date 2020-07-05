from copy import copy
from itertools import product, combinations
import random

def pareto_dominates(new_val, old_val):
	failed = False
	reallyGained = False
	for player in range(players):
		if new_val[player] < old_val[player]:
			failed = True
		elif new_val[player] > old_val[player]:
			reallyGained = True

	return reallyGained and not failed


players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

items = 9
all_combs = [item for item in product([i for i in range(players)], repeat=items)]


def value_fix(valuations):
	for player in valuations:
		for elem in range(items):
			valuations[player][elem] += 0.0001

	return valuations

def value_fix2(valuations):
	for player in valuations:
		for elem in range(items):
			if valuations[player][elem] == 0:
				valuations[player][elem] = random.random() / (1000 * 1000)

	return valuations

def value_fix3(valuations, epsilon):
	for player in valuations:
		for elem in range(items):
			valuations[player][elem] += epsilon * 2**elem

	return valuations

efx_combs = []

valuations = {0: [1.02, 5.01, 1, 1, 3,0.009,0.009,0,0.01], 1: [1, 0.375, 1.15, 0.125, 0.125,0,0,0,0], 2: [1, 5.01, 3, 3, 1.1,0.01,0.1,0.01,0]}


epsilon = 1/(1000 * 2000)

#valuations = value_fix3(valuations, epsilon)
#valuations = value_fix2(valuations)


# check for EFX combs - no one is jealous of anyone else in the combination after reducing any one item
for comb in all_combs:
	all_poss_j = []
	isAlreadyJealous = False
	for observer, counterpart in all_pairs:
		side1_items = []
		side2_items = []
		for i in range(len(comb)):
			if comb[i] == observer:
				side1_items.append(i)
			elif comb[i] == counterpart:
				side2_items.append(i)
		val_side1 = 0

		# add all side 1 values
		for side1_item in side1_items:
			val_side1 += valuations[observer][side1_item]

		# consider any item to remove from side 2
		for j in range(len(side2_items)):
			val_side2 = 0

			# add all side 2 values omitting the item indexed j, according to 
			for side2_item in (side2_items[:j] + side2_items[j+1:]):
				val_side2 += valuations[observer][side2_item]

			if val_side2 > val_side1:
				# This is not an EFX comb - there is some envious agent
				isAlreadyJealous = True

	if isAlreadyJealous == False:
		efx_combs.append(comb)

efx_valuations = []
for comb in efx_combs:
	new_val = []
	for player in range(players):
		player_value = 0
		for elem_ind in range(len(comb)):
			if comb[elem_ind] == player:
				player_value += valuations[player][elem_ind]

		new_val.append(player_value)
	efx_valuations.append([new_val, comb])

#print(efx_valuations)


for comb in all_combs:
	new_val = []
	for player in range(players):
		player_value = 0
		for elem_ind in range(len(comb)):
			if comb[elem_ind] == player:
				player_value += valuations[player][elem_ind]

		new_val.append(player_value)

	new_efx_valuations = []
	for e_val, e_comb in efx_valuations:
		if not pareto_dominates(new_val, e_val):
			new_efx_valuations.append([e_val, e_comb])

		# The current combination pareto dominates the EFX combination e_comb, not adding it to the next round 
		#else:
			#print("EFX comb {} with values {} superseded by {} due to combination {}".format(e_comb, e_val, new_val, comb))
	efx_valuations = new_efx_valuations

	if efx_valuations == []:
		print("REALLY??")
		import pdb
		pdb.set_trace()
		break
print(efx_valuations)
