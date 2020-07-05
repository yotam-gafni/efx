import random
from itertools import product, combinations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import time


arrays = []

comb_behavior = {}

def pareto_dominates(new_val, old_val):
	failed = False
	reallyGained = False
	for player in range(players):
		if new_val[player] < old_val[player]:
			failed = True
		elif new_val[player] > old_val[player]:
			reallyGained = True

	return reallyGained and not failed

def generate_valuation(base):
	variable_string = "{"
	variables = []
	constraint_string = ""
	constraints = []

	for item in range(items):
		variables.append("x{}".format(item))


	for elem in base:
		con_string = ""
		for item in range(items):
			if elem[item] == 1:
				con_string += "+ x{}".format(item)
			elif elem[item] == -1:
				con_string += "- x{}".format(item)
		constraints.append(con_string + " < 0")

	opt_goal = "5"

	constraint_string = "{" + ",".join(constraints) + "}"

	variable_string += ",".join(variables) + "}"

	lp_string = "Quiet[Maximize[" + opt_goal + ", " + constraint_string + "," + variable_string + "]]"

	try:
		is_feasible = session.evaluate(wlexpr(lp_string))

		valuation = []

		for item in range(items):
			if type(is_feasible[1][item][1]) == int:
				valuation.append(is_feasible[1][item][1])
			else:
				try:
					valuation.append(is_feasible[1][item][1][0] / is_feasible[1][item][1][1])
				except Exception as e:
					for i in range(1000):
						print("UNFEASIBLE CONSTRAINTS!!!!")
						return None
	except Exception as e:
		print("EXCEPTION IN GENERATE VALUATION")
		import pdb
		pdb.set_trace()

	return valuation


def reverse_comb(comb):
	new_comb = []
	for i in comb:
		new_comb.append(-i)

	return new_comb

def is_comb_in_base(comb, base):
	variable_string = "{"
	variables = []
	constraint_string = ""
	constraints = []
	item_constraints = ["" for j in range(len(comb))]
	for i in range(len(base)):
		variables.append("x{}".format(i))
		constraints.append("x{} >= 0".format(i))
		for j in range(len(comb)):
			if base[i][j] == 1:
				item_constraints[j] += "+ x{}".format(i)
			elif base[i][j] == -1:
				item_constraints[j] += " - x{}".format(i)


	opt_goal = item_constraints[0]
	for j in range(len(comb)):
		item_constraints[j] += " == {}".format(comb[j])

	all_constraints = item_constraints + constraints

	constraint_string = "{" + ",".join(all_constraints) + "}"

	variable_string += ",".join(variables) + "}"

	lp_string = "Quiet[Maximize[" + opt_goal + ", " + constraint_string + "," + variable_string + "]]"

	is_feasible = session.evaluate(wlexpr(lp_string))


	return type(is_feasible[0]) == int


#is_comb_in_base([0,0,1,-1,1,0],[[-1, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0], [0, 0, 0, -1, 0, 0], [0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, -1], [1, -1, -1, 0, 0, 1], (1, -1, 1, -1, 0, 0), (-1, 1, 0, -1, 0, 1), [1, 0, -1, -1, 1, 1], [1, -1, -1, 1, 0, -1], [0, 0, -1, 0, 0, 1], [1, 1, -1, -1, -1, 1], [1, 0, -1, 0, 1, 0], [0, -1, -1, 1, 1, 0], (0, -1, -1, -1, -1, 1), (1, 1, -1, 0, 0, 0), (-1, 0, 0, -1, 1, 1), (-1, 1, -1, 1, 0, -1), (-1, 0, -1, 0, 0, 0), (-1, 1, 0, 0, 0, -1), (1, 1, 1, -1, -1, -1), (0, 0, 0, 0, -1, 1), (-1, 1, 0, -1, 0, 0), [0, 0, 1, -1, 1, 0], [0, 1, 1, -1, 0, -1], [0, -1, -1, 0, 0, -1], (-1, 1, 1, 1, 1, 0), [0, 1, 0, 0, 0, -1], [1, 0, -1, 1, 0, 0], [-1, 0, -1, 1, 1, 0], (0, 1, 1, -1, 0, 0), (0, 0, 1, -1, 0, -1), [1, -1, 1, 0, -1, 0], [1, -1, 0, 0, 1, 1], [0, 0, -1, 1, 1, 0], [0, 0, 1, 1, 1, 1], (0, -1, 0, -1, 0, 1), (-1, -1, -1, 1, 1, -1), [0, -1, -1, 1, -1, -1], [1, 0, 0, -1, -1, 0], (0, -1, 0, -1, 1, 0), [0, -1, -1, 0, -1, 1], [1, -1, 1, 1, 0, -1], [-1, 1, 0, 0, -1, 1], (1, 1, 0, -1, -1, 0), (-1, -1, -1, 0, 0, 1), [-1, 0, 0, 0, -1, -1], [-1, 1, 1, -1, 1, 1], [1, 0, -1, 0, 0, 0], [0, -1, -1, 0, -1, 0], (0, 0, 1, 0, 1, -1), (1, -1, 1, 0, 1, -1), (1, 1, 1, 1, 1, -1), [-1, 1, 1, 1, 0, -1], (-1, -1, -1, 1, 1, 0), (-1, -1, 0, 1, -1, -1), (1, 1, -1, 1, 0, -1), (-1, 0, 0, 1, 0, 1), [1, -1, -1, 1, 0, 0], [0, 1, -1, 0, 0, -1], [1, 1, 1, -1, 0, 0], (-1, -1, 1, 0, 0, 0), (1, 0, -1, 0, 1, -1), (0, -1, 1, 1, -1, -1), (0, -1, 0, -1, -1, 1), [1, 0, 1, -1, 1, 1], [-1, 1, 0, 1, 0, -1], [1, 1, 1, 0, -1, 1], (-1, 1, 0, -1, 0, -1), [-1, 0, 1, -1, 1, 0], [0, -1, 0, -1, -1, 1], (1, 0, 0, 1, 1, -1), [-1, -1, 1, -1, -1, -1], (1, 1, -1, 0, 0, -1), [0, 0, 1, 0, 0, 1], (-1, -1, 1, -1, 1, 0), [0, -1, 0, -1, 1, 0], (-1, 1, 0, 0, -1, 0), (1, -1, 1, 1, 1, -1), [0, 0, 0, -1, 0, 0], (0, 1, 0, 0, 0, -1), (-1, 1, -1, 1, -1, 1), (1, 1, 1, -1, 1, -1), [0, 0, 0, -1, -1, 0], (-1, 1, -1, -1, -1, 1), [0, -1, -1, 0, 1, 1], [1, 0, 0, 1, 0, 1], [1, 1, -1, -1, -1, 0], [1, -1, -1, 1, 1, 0], [-1, -1, -1, 1, 0, 0], (-1, 1, -1, 1, -1, -1), (0, 0, 0, 1, 1, -1), [-1, -1, 1, 0, -1, 0], [0, 0, 0, -1, 1, 0], [1, -1, 1, 0, 0, 1], (1, 0, 0, 1, 1, 1), (0, -1, 0, 0, -1, 0), [-1, 1, 1, -1, 1, 0], [-1, 0, -1, 0, 1, -1], (-1, 0, 0, -1, -1, 0), (0, 1, 0, 1, 0, 1), [-1, 1, 1, 0, 1, 0], (1, -1, 1, -1, 1, 1), [-1, 1, 1, 0, 1, 1], (1, 1, 0, -1, -1, -1), [-1, -1, 0, 1, 1, -1], (1, 1, -1, -1, 0, 1), (1, 0, 1, -1, 1, 1), (1, 0, -1, -1, -1, -1), (-1, 1, 1, 1, 0, 1), (1, 1, -1, 0, 0, 1), (-1, 0, -1, -1, 0, 1), [0, -1, 1, 1, 0, 1], (0, 1, 1, 1, -1, -1), [-1, -1, -1, -1, 1, 0], [-1, 1, 1, 1, -1, -1], [-1, -1, 1, -1, 1, 0], (1, 0, -1, 1, -1, -1), [0, -1, 0, 0, 1, 1], [0, 0, 1, 0, 1, -1], [-1, -1, -1, 1, -1, 0], [1, -1, 0, 1, -1, 0], [0, -1, -1, 1, -1, 1], [-1, -1, -1, 0, 1, 0], [1, 0, -1, -1, 0, 0], [-1, 1, -1, 0, 0, 0], (0, 0, 1, -1, 1, 1), (0, -1, -1, 0, 0, 0), [-1, 1, -1, -1, -1, 0], [0, 1, 0, 1, 0, 0], [-1, 1, 1, -1, 1, -1], (1, 1, 1, 1, -1, 1), [1, 1, -1, -1, 0, -1], [-1, -1, 0, -1, -1, 1], [-1, 0, -1, 0, -1, 0], [1, 0, 1, -1, 0, 0], [1, -1, 1, 1, 1, 1], [-1, 1, -1, 0, 0, -1], [0, -1, 1, 0, 1, -1], [-1, 0, -1, 1, -1, 0], (0, -1, 0, -1, 1, 1), [-1, 0, 0, -1, -1, 0], [-1, -1, 0, -1, 0, -1], [0, 1, 1, 0, 1, 1], [-1, 0, 1, -1, 1, -1], [-1, 0, 0, 0, 0, -1], (-1, 1, 1, -1, 1, 1), (0, -1, 0, 0, 1, 0), (-1, 0, 1, 0, -1, -1), [1, 1, 1, 1, 1, 1], [-1, 0, 0, 1, -1, 1], (0, -1, -1, -1, 0, -1), [-1, 0, 1, -1, 0, -1], [-1, 1, 1, 0, 0, 0], [1, -1, 0, 1, -1, 1], [0, 0, 1, 0, -1, 0], (1, 1, 0, 1, -1, 0), (0, 1, 0, -1, -1, 1), [1, 1, 1, 0, 1, 1], (-1, 1, 1, 1, 0, -1), (-1, -1, -1, -1, 1, 0), [0, 1, -1, -1, 1, 0], (1, 1, 0, -1, 0, -1), (0, 1, -1, 1, -1, -1), [1, 1, 1, 0, 1, 0], (-1, -1, 0, 0, 1, 1), (1, 1, -1, -1, -1, 0), [0, -1, 1, 1, -1, -1], (1, 1, 0, 1, 0, -1), [1, 0, 1, -1, 0, 1], [1, -1, -1, 0, 1, 1], [1, 1, 0, -1, 0, 0], (1, -1, 0, 0, -1, 0), (0, 0, 1, 1, -1, 0), (-1, 0, 1, 0, 0, 1), (1, -1, -1, 1, 0, -1), (1, -1, -1, 1, 1, 0), [0, -1, 1, 0, 1, 0], (0, -1, 1, 1, 0, 1), [0, 1, 0, 0, 0, 0], (-1, 1, -1, 1, -1, 0), (-1, 0, 1, -1, 0, -1), [1, 1, 0, 0, 0, 1], [1, 1, -1, 1, 1, 0], (-1, -1, 1, 0, 0, 1), (0, 1, 1, 0, 0, -1), (1, 1, 0, 0, 1, 0), (1, 0, 0, 0, 1, 0), [-1, -1, 1, -1, 1, 1], (0, 1, -1, -1, 0, 1), (-1, 0, 1, 1, 1, -1), [1, 1, -1, 1, 1, -1], [-1, 0, -1, -1, 1, 0], [0, 1, 1, -1, 0, 0], (1, 0, -1, 1, 0, -1), (1, -1, 0, 0, -1, 1), (-1, -1, 1, -1, 0, -1), (-1, 1, 1, -1, -1, -1), (0, 0, -1, -1, 0, -1), (1, 1, -1, 0, -1, -1), [0, -1, 0, 1, 0, 1], (-1, 1, 0, -1, -1, 0), (0, 1, 1, 1, 1, 1), (1, 1, 1, 0, 1, 1), (1, -1, -1, 0, 1, -1), [0, 0, 1, 0, 0, -1], (0, -1, -1, 0, 0, -1), [0, -1, -1, -1, -1, 0], [1, 1, -1, -1, 0, 1], (-1, -1, -1, -1, 0, 1), (-1, -1, 1, -1, 1, -1), [1, 0, 0, -1, 0, 1], [1, 0, 0, 1, 1, 1], [1, -1, -1, -1, 0, 0], [-1, 0, -1, 0, 0, 1], [-1, 0, 1, 1, -1, 0], [-1, 0, 1, 0, 1, -1], [0, 1, -1, 1, -1, -1], [-1, -1, 0, 0, 1, 1], [1, -1, 1, -1, -1, -1], [-1, -1, 1, 0, 1, -1], [-1, 0, -1, 0, 0, -1], [0, -1, 1, 1, 0, 0], [1, 1, 0, -1, -1, -1], (1, 0, -1, 0, 0, 0), [-1, 0, 1, 0, 1, 0], [0, 1, 1, 0, -1, -1], (1, 1, 0, 0, 0, 1), [-1, -1, -1, 0, 0, 0], (-1, -1, 0, -1, 0, 0), [0, -1, 0, -1, 0, 0], (-1, -1, 1, 0, -1, 0), [-1, 1, 0, -1, 0, 1], (1, -1, 1, 0, -1, 0), [1, 1, -1, 0, 0, 1], (1, 0, 1, 0, 1, -1), [1, 0, 0, 0, -1, 0], [-1, 0, 0, 0, 1, 1], [1, 1, 0, -1, 0, -1], (-1, 0, 0, -1, 1, 0), (-1, -1, 1, 0, 1, 1), (0, -1, 1, -1, 0, -1), (1, -1, 0, -1, 1, 1), [0, 0, -1, -1, 1, -1], (-1, -1, 0, -1, 0, -1), (-1, 1, 1, 0, -1, 0), (-1, 0, -1, 0, 1, 1), [-1, -1, -1, 0, -1, 0], (0, 1, 1, -1, 0, -1), (-1, 0, 0, 0, 0, -1), (0, -1, -1, -1, 1, 1), [-1, 0, 1, 0, -1, -1], (-1, -1, 0, -1, 1, -1), [0, 1, -1, 1, -1, 0], (-1, -1, -1, 0, 0, 0), [0, 0, 1, -1, -1, 0], [0, 0, 1, 0, 0, 0], [0, 0, -1, 0, 1, 1], [0, -1, 0, 0, -1, 1], [0, -1, -1, -1, -1, 1], [1, 0, -1, 0, -1, 1], [0, -1, -1, 1, 1, -1], [0, 1, 0, 1, 1, 1], [0, 1, 0, -1, 1, -1], [1, 0, 1, -1, -1, 1], (1, 0, -1, 1, 1, 1), [0, -1, 1, 0, -1, -1], (1, 0, -1, 1, 1, 0), (1, 0, 1, -1, 0, -1), (1, -1, 1, 0, 1, 0), [0, 0, 0, -1, 0, -1], (0, -1, 0, 0, 0, -1), (0, 1, 1, -1, -1, -1), (1, 0, 1, 0, -1, -1), (1, 0, 0, 0, 1, -1), (-1, -1, -1, 1, -1, -1), [-1, 1, -1, 1, 0, -1], (-1, -1, 0, -1, 0, 1), [0, -1, 1, -1, -1, 0], (-1, 1, 0, 0, 1, 0), (1, -1, -1, -1, -1, 1), (0, 1, -1, 0, 1, -1), [1, -1, 0, 1, -1, -1], [0, -1, -1, -1, 1, 0], [-1, 1, 0, 0, 0, 0], [0, 1, 0, 0, -1, -1], [0, 1, 0, 1, 1, 0], [0, 0, -1, 0, -1, 0], [-1, 1, 1, 0, -1, 0], [1, 0, 1, 1, -1, 1], (-1, -1, 1, 0, 1, 0), (0, -1, 1, 1, 0, -1), [-1, -1, 1, 1, 1, 1], [1, -1, -1, 0, -1, 1], [-1, -1, 0, 0, 1, 0], (1, 0, 1, 0, 1, 1), (1, 0, -1, -1, -1, 0), [0, 1, 0, 1, -1, 1]])

def is_pareto_dominable(alloc, true_combs_base, all_combs):
	players = len(true_combs_base)
	items = len(alloc)

	all_zeros = [0 for j in range(items)]


	for comb in  all_combs:
		eq_by_player = [copy(all_zeros) for i in range(players)]

		for i in range(items):
			if alloc[i] != comb[i]:
				eq_by_player[alloc[i]][i] = 1
				eq_by_player[comb[i]][i] = -1

		isPD = True
		isSPD = False
		for player in range(players):
			if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
				isPD = False
				break
			elif is_comb_in_base(eq_by_player[player], true_combs_base[player]):
				isSPD = True
				continue
			anti_comb = reverse_comb(eq_by_player[player])
			if is_comb_in_base(anti_comb, true_combs_base[player]):
				isPD = False
				break
			else:
				isSPD = True

		if isPD and isSPD:
			return True, eq_by_player

	return False, None

def is_pareto_dominated(alloc, true_combs_base, all_combs, good_combs):
	players = len(true_combs_base)
	items = len(alloc)

	all_zeros = [0 for j in range(items)]
	all_combs_copy = copy(all_combs)

	random.shuffle(all_combs_copy)

	running_ind = 0
	how_many = 0

	bad_combs = {0: set([]), 1: set([]), 2:set([])}



	for comb in  all_combs_copy:
		running_ind += 1
		eq_by_player = [copy(all_zeros) for i in range(players)]

		for i in range(items):
			if alloc[i] != comb[i]:
				eq_by_player[alloc[i]][i] = 1
				eq_by_player[comb[i]][i] = -1

		isPD = True
		isSPD = False
		more_thorough = []
		for player in range(players):
			if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
				continue
			elif 1 not in eq_by_player[player]:
				isSPD = True
				continue
			elif -1 not in eq_by_player[player]:
				isPD = False
			else:
				more_thorough.append(player)
		
		if isPD:
			for player in more_thorough:
				how_many += 1
				if tuple(eq_by_player[player]) in good_combs[player]:
					isSPD = True
					continue

				elif tuple(eq_by_player[player]) in bad_combs[player]:
					isPD = False
					break

				if is_comb_in_base(eq_by_player[player], true_combs_base[player]):
					isSPD = True
					good_combs[player].add(tuple(eq_by_player[player]))
					continue
				else:
					isPD = False
					bad_combs[player].add(tuple(eq_by_player[player]))
					break

		if isPD and isSPD:
			#print("FOUND PD IN RUN INDEX {}".format(running_ind))
			print("HOW MANY: {}".format(how_many))
			return True

	#print("NOT PD")
	print("HOW MANY: {}".format(how_many))

	return False

def filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs, bad_combs):
	filtered_allocs = []
	players = len(true_combs_base)
	items = len(allocs[0])

	all_zeros = [0 for j in range(items)]
	all_combs_copy = copy(all_combs[:500])

	random.shuffle(all_combs_copy)

	running_ind = 0
	how_many = 0


	bad_combs = {0: set([]), 1: set([]), 2:set([])}

	for alloc in allocs:
		foundPD = False
		for comb in  all_combs_copy:
			running_ind += 1
			eq_by_player = [copy(all_zeros) for i in range(players)]

			for i in range(items):
				if alloc[i] != comb[i]:
					eq_by_player[alloc[i]][i] = 1
					eq_by_player[comb[i]][i] = -1

			isPD = True
			isSPD = False
			more_thorough = []
			for player in range(players):
				if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
					continue
				elif 1 not in eq_by_player[player]:
					isSPD = True
					continue
				elif -1 not in eq_by_player[player]:
					isPD = False
					break
				else:
					more_thorough.append(player)
			
			if isPD: 
				for player in more_thorough:
					how_many += 1
					if tuple(eq_by_player[player]) in good_combs[player]:
						isSPD = True
						continue

					elif tuple(eq_by_player[player]) in bad_combs[player]:
						isPD = False
						break

					if is_comb_in_base(eq_by_player[player], true_combs_base[player]):
						isSPD = True
						good_combs[player].add(tuple(eq_by_player[player]))
						continue
					else:
						isPD = False
						bad_combs[player].add(tuple(eq_by_player[player]))
						break

			if isPD and isSPD:
				#print("FOUND PD IN RUN INDEX {}".format(running_ind))
				#print("HOW MANY: {}, FILTERED LENGTH: {}".format(how_many, len(filtered_allocs)))
				foundPD = True
				break

		#print("NOT PD")
		if not foundPD:
			filtered_allocs.append(alloc)
		#print("HOW MANY: {}, FILTERED LENGTH: {}".format(how_many, len(filtered_allocs)))

	return filtered_allocs

def filter_efx_envious(allocs, true_combs_base, all_combs, good_combs, bad_combs):
	filtered_allocs = []
	for alloc in allocs:
		all_poss_j = []
		for pair in all_pairs:
			side1_items = []
			side2_items = []
			equ = copy(all_zeros)
			for i in range(len(alloc)):
				if alloc[i] == pair[0]:
					side1_items.append(i)
					equ[i] = 1
				elif alloc[i] == pair[1]:
					side2_items.append(i)
					equ[i] = -1

			for j in side2_items:
				curr_equ = copy(equ)
				curr_equ[j] = 0
				if sum(curr_equ) == 0 and len(set(curr_equ)) == 1:
					continue
				all_poss_j.append(tuple([pair[0], curr_equ]))

		random.shuffle(all_poss_j)
		isAlreadyJealous = False
		count_ops = 0
		for elem in all_poss_j:
			#anti_comb = reverse_comb(elem[1])
			if tuple(elem[1]) in good_combs[elem[0]]: 
				#print("alloc {} has eq {} for player {}, and thus envious".format(alloc, elem[1], elem[0]))
				isAlreadyJealous = True
				break
			elif tuple(elem[1]) in bad_combs[elem[0]]:
				continue
			elif is_comb_in_base(tuple(elem[1]), true_combs_base[elem[0]]):
				count_ops += 1
				good_combs[elem[0]].add(tuple(elem[1]))
				isAlreadyJealous = True
				break
			else:
				bad_combs[elem[0]].add(tuple(elem[1]))
				continue
		if isAlreadyJealous == False:
			#print("alloc {} has no current envy, performed {} ops".format(alloc, count_ops))
			filtered_allocs.append(alloc)

	return filtered_allocs


def split_mandatory(all_combs):
	mandatory_combs = []
	later_combs = []
	latest_combs = []

	for comb in all_combs:
		counts = [0,0,0]
		counts[0] = len([i for i in filter(lambda x: x==0, comb)])
		counts[1] = len([i for i in filter(lambda x: x==1, comb)])
		counts[2] = len([i for i in filter(lambda x: x==2, comb)])

		counts.sort()
		if counts[:2] == [1,1]:
			mandatory_combs.append(comb)
		elif 1 in counts:
			later_combs.append(comb)
		elif 0 not in counts:
			latest_combs.append(comb)

	return mandatory_combs, later_combs, latest_combs



players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

for items in range(8,13):

	all_combs = [item for item in product([i for i in range(players)], repeat=items)]

	mandatory_combs, later_combs, latest_combs = split_mandatory(all_combs)

	max_stop = 0
	max_conf = {}

	for random_try in range(1000):

		print("RANDOM TRY: {}".format(random_try))
		true_combs_base = dict()



		all_zeros = [0 for j in range(items)]
		good_combs = {0: set([]), 1: set([]), 2: set([])}
		evil_combs = {0: set([]), 1: set([]), 2: set([])}

		for i in range(players):
			true_combs_base[i] = []
			for j in range(items):
				unit_vector = copy(all_zeros)
				unit_vector[j] = -1
				true_combs_base[i].append(unit_vector)
				good_combs[i].add(tuple(unit_vector))
				anti_v = reverse_comb(unit_vector)
				evil_combs[i].add(tuple(anti_v))

		random.shuffle(later_combs)
		random.shuffle(latest_combs)
		random.shuffle(mandatory_combs)


		running_ind = 0
		failed_run = False

		stage = "MANDATORY"


		relevant_combs = []

		for comb in mandatory_combs:
			running_ind += 1
			const_num = 0
			for player in range(players):
				const_num += len(true_combs_base[player])
			if running_ind % 10 == 0:
				print("ITEMS: {}, STAGE: {}, ATTEMPT {}, COMBINATION NUM {}, CONSTRAINT NUMBER {}".format(items, stage, random_try,running_ind, const_num))

			#if running_ind >= len(mandatory_combs):
			#	print("FINISHED MANDATORY CONSTRAINTS")

			start = time.time()

			all_poss_j = []
			for pair in all_pairs:
				side1_items = []
				side2_items = []
				equ = copy(all_zeros)
				for i in range(len(comb)):
					if comb[i] == pair[0]:
						side1_items.append(i)
						equ[i] = 1
					elif comb[i] == pair[1]:
						side2_items.append(i)
						equ[i] = -1

				for j in side2_items:
					curr_equ = copy(equ)
					curr_equ[j] = 0
					if sum(equ) == 0 and len(set(equ)) == 1:
						continue
					all_poss_j.append(tuple([pair[0], curr_equ]))

			random.shuffle(all_poss_j)

			isAlreadyJealous = False
			for elem in all_poss_j:
				#anti_comb = reverse_comb(elem[1])
				if is_comb_in_base(elem[1], true_combs_base[elem[0]]):
					isAlreadyJealous = True
					break

			after_efx_check = time.time()
			print("EFX CHECK TOOK {}".format(after_efx_check - start))

			if running_ind >= len(mandatory_combs):
				if is_pareto_dominated(comb, true_combs_base, all_combs, good_combs):
					continue

			after_pareto_check = time.time()
			print("PARETO CHECK TOOK {}".format(after_pareto_check - after_efx_check))

			if isAlreadyJealous == False:
				for elem in all_poss_j:
					anti_comb = reverse_comb(elem[1])
					if not is_comb_in_base(anti_comb, true_combs_base[elem[0]]):
						#anti_comb = reverse_comb(elem[1])
						true_combs_base[elem[0]].append(elem[1])
						const_num = 0
						for player in range(players):
							const_num += len(true_combs_base[player])
						print("ADDED EQUATION {}, now have {} constraints".format(elem[1], const_num))
						isAlreadyJealous = True

						break

			after_efx_addition = time.time()
			print("EFX ADDITION TOOK {}".format(after_efx_addition - after_pareto_check))

			if isAlreadyJealous == False:
				res, add_equations = is_pareto_dominable(comb, true_combs_base, all_combs)
				after_pareto_addition = time.time()
				print("PARETO ADDITION TOOK {}".format(after_pareto_addition - 	after_efx_addition))

				if res:
					for player in range(players):
						true_combs_base[player].append(add_equations[player])
				else:
					max_stop = max(max_stop, running_ind)
					print("RANDOM TRY: {}, FAILED ON COMBINATION {}/{}, MAX SUCCESS {}/{}".format(random_try,running_ind,players**items,max_stop, players**items))
					break

			if running_ind > players**items - 5:
				valuations = {0: [], 1: [], 2:[]}

				for player in range(players):
					valuations[player] = generate_valuation(true_combs_base[player])

				print(valuations)
				print("GREAT SUCCESS")
				import pdb
				pdb.set_trace()

		allocs = later_combs + latest_combs
		stage = "FINAL"
		while True:
			votes = {}

			begin_length = len(allocs)

			valuations = {0: [], 1: [], 2:[]}

			for player in range(players):
				valuations[player] = generate_valuation(true_combs_base[player])

			bad_combs = {0: set([]), 1: set([]), 2:set([])}
			
			random.shuffle(allocs)

			sampled_allocs = allocs[:500]

			print("ALLOCS BEFORE FILTER {}".format(len(allocs)))
			fs_allocs = filter_pareto_dominated(sampled_allocs, true_combs_base, all_combs, good_combs, bad_combs)
			print("ALLOCS AFTER PARETO FILTER {}".format(len(allocs)))
			fe_allocs = filter_efx_envious(fs_allocs, true_combs_base, all_combs, good_combs, bad_combs)
			#print("ALLOCS AFTER EFX FILTER {}".format(len(allocs)))


			valuations = {0: [], 1: [], 2:[]}

			for player in range(players):
				valuations[player] = generate_valuation(true_combs_base[player])


			start = time.time()

			#all_poss_j = []
			for alloc in fe_allocs:
				for pair in all_pairs:
					side1_items = []
					side2_items = []
					equ = copy(all_zeros)
					for i in range(len(comb)):
						if alloc[i] == pair[0]:
							side1_items.append(i)
							equ[i] = 1
						elif alloc[i] == pair[1]:
							side2_items.append(i)
							equ[i] = -1

					for j in side2_items:
						curr_equ = copy(equ)
						curr_equ[j] = 0
						if sum(equ) == 0 and len(set(equ)) == 1:
							continue
						if tuple([pair[0], tuple(curr_equ)]) in votes:
							votes[tuple([pair[0],tuple(curr_equ)])] += 1
						else:
							votes[tuple([pair[0],tuple(curr_equ)])] = 1
						#all_poss_j.append(tuple([pair[0], curr_equ]))

				#random.shuffle(all_poss_j)
			sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True) 
			#print(sorted_votes)
			for key, val in sorted_votes:
				if tuple(key[1]) in good_combs[key[0]]:
					continue
				anti_key = tuple(reverse_comb(key[1]))
				if tuple(anti_key) in evil_combs[key[0]]:
					continue
				elif is_comb_in_base(anti_key, true_combs_base[key[0]]):
					evil_combs[player].add(anti_key)
				else:
					valuations= generate_valuation(true_combs_base[key[0]] + [tuple(key[1])])
					if valuations is None:
						import pdb
						pdb.set_trace()

					good_combs[key[0]].add(tuple(key[1]))
					true_combs_base[key[0]].append(tuple(key[1]))
					break


			allocs = fe_allocs + allocs[501:]

			end_length = len(allocs)
			print("COVERED {}/{} ALLOCATIONS".format(players**items - len(allocs), players**items))
			running_ind += 1
			const_num = 0
			for player in range(players):
				const_num += len(true_combs_base[player])
			if running_ind % 10 == 0:
				print("ITEMS: {}, STAGE: {}, ATTEMPT {}, COMBINATION NUM {}, CONSTRAINT NUMBER {}, GOOD+EVIL = {}, VOTES = {}".format(items, stage, random_try,running_ind, const_num, sum([len(good_combs[player])+len(evil_combs[player]) for player in range(3)]), len(votes)))



			if begin_length == end_length:
				print("STUCK, MOVING TO PARETO ADDITION AFTER COMPLETING {}/{}".format(players**items - len(allocs), players**items))
				valuations = {0: [], 1: [], 2:[]}

				for player in range(players):
					valuations[player] = generate_valuation(true_combs_base[player])

				print(valuations)
				break

			if len(allocs) == 0:
				valuations = {0: [], 1: [], 2:[]}

				for player in range(players):
					valuations[player] = generate_valuation(true_combs_base[player])

				print(valuations)
				print("GREAT SUCCESS")
				import pdb
				pdb.set_trace()

		while allocs:
			begin_length = len(allocs)
			for alloc in allocs:
				res, add_equations = is_pareto_dominable(allocs[0], true_combs_base, all_combs)

				if res:
					for player in range(players):
						if add_equations[player] == [0] * items:
							print("ZERO EQUATION ENCOUNTERED")
							import pdb
							pdb.set_trace()
						true_combs_base[player].append(add_equations[player])
					break

			bad_combs = {0: set([]), 1: set([]), 2:set([])}

			allocs = filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs, bad_combs)
			end_length = len(allocs)

			if begin_length == end_length:
				print("STUCK, WRAPPING UP AFTER COMPLETING {}/{}".format(players**items - len(allocs), players**items))
				valuations = {0: [], 1: [], 2:[]}

				for player in range(players):
					valuations[player] = generate_valuation(true_combs_base[player])

				print(valuations)
				break
