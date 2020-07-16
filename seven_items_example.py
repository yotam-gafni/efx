import random
from itertools import product, combinations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import time


arrays = []

comb_behavior = {}

global lp_runs
lp_runs = 0

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
	global lp_runs
	lp_runs += 1

	if lp_runs % 1000 == 0:
		print("LP_RUNS: {}".format(lp_runs))

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
	all_combs_copy = copy(all_combs)

	random.shuffle(all_combs_copy)

	running_ind = 0
	how_many = 0


	bad_combs = {0: set([]), 1: set([]), 2:set([])}

	for alloc in allocs:
		print("Pareto filter alloc number {}".format(int(running_ind/3**items)))
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
				#print("alloc {} is pareto dominated by comb {}, removing".format(alloc, comb))
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
				#print("alloc {} has eq {} for player {}, and thus envious".format(alloc, elem[1], elem[0]))
				isAlreadyJealous = True
				break
			else:
				bad_combs[elem[0]].add(tuple(elem[1]))
				continue
		if isAlreadyJealous == False:
			#print("alloc {} has no current envy, performed {} ops".format(alloc, count_ops))
			filtered_allocs.append(alloc)

	return filtered_allocs

def autocorr(f_votes, tcb, player):
	count_bad = 0
	for f_vote in f_votes:
		try:
			if f_vote[0] == player:
				anti_fvote = tuple(reverse_comb(f_vote[1]))
				if is_comb_in_base(anti_fvote, tcb):
					count_bad += 1
		except Exception as e:
			print("WAT")
			import pdb
			pdb.set_trace()

	return count_bad


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

def only_2_2_3(all_combs):
	reduced = []
	for comb in all_combs:
		counts = [0,0,0]
		counts[0] = len([i for i in filter(lambda x: x==0, comb)])
		counts[1] = len([i for i in filter(lambda x: x==1, comb)])
		counts[2] = len([i for i in filter(lambda x: x==2, comb)])

		counts.sort()

		if counts == [2,2,3]:
			reduced.append(comb)

	return reduced


players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

for items in range(7,8):

	all_combs = [item for item in product([i for i in range(players)], repeat=items)]
	all_eqs = [item for item in product([-1,0,1], repeat=items)]




	max_stop = 0
	max_conf = {}

	for random_try in range(1000):

		allocs = only_2_2_3(all_combs)


		print("RANDOM TRY: {}".format(random_try))
		true_combs_base = {0: [], 1: [], 2: []}



		all_zeros = [0 for j in range(items)]
		good_combs = {0: set([]), 1: set([]), 2: set([])}
		evil_combs = {0: set([]), 1: set([]), 2: set([])}

		for eq in all_eqs:
			counts = [0,0,0]
			counts[0] = len([i for i in filter(lambda x: x==-1, eq)])
			counts[1] = len([i for i in filter(lambda x: x==0, eq)])
			counts[2] = len([i for i in filter(lambda x: x==1, eq)])

			if (counts[0] == 1 and counts[2] == 0) or (counts[0] == 2 and counts[2] == 1):
				if eq[0] != 1:
					for j in range(3):
						true_combs_base[j].append(eq)
						good_combs[j].add(tuple(eq))
						anti_eq = reverse_comb(eq)
						evil_combs[j].add(tuple(anti_eq))
				else:
					if eq == [1, 0, -1, 0, -1, 0, 0]:
						for j in [1,2]:
							true_combs_base[j].append(eq)
							good_combs[j].add(tuple(eq))
							anti_eq = reverse_comb(eq)
							evil_combs[j].add(tuple(anti_eq))
						true_combs_base[0].append(anti_eq)
						good_combs[0].add(tuple(anti_eq))
						evil_combs[0].add(tuple(eq))
					elif eq == [1, -1, 0, 0, 0, -1, 0]:
						for j in [0,2]:
							true_combs_base[j].append(eq)
							good_combs[j].add(tuple(eq))
							anti_eq = reverse_comb(eq)
							evil_combs[j].add(tuple(anti_eq))
						true_combs_base[1].append(anti_eq)
						good_combs[1].add(tuple(anti_eq))
						evil_combs[1].add(tuple(eq))
					elif eq == [1, 0, 0, -1, -1, 0, 0]:
						for j in [1,2]:
							true_combs_base[j].append(eq)
							good_combs[j].add(tuple(eq))
							anti_eq = reverse_comb(eq)
							evil_combs[j].add(tuple(anti_eq))
						true_combs_base[1].append(anti_eq)
						good_combs[1].add(tuple(anti_eq))
						evil_combs[1].add(tuple(eq))	
					else:
						for j in [0,1,2]:
							true_combs_base[j].append(eq)
							good_combs[j].add(tuple(eq))
							anti_eq = reverse_comb(eq)
							evil_combs[j].add(tuple(anti_eq))

		perm = [0,1,2,3,4,5,6]
		preamble = [0,1]
		postamble = [2,3,4,5,6]
		for j in range(3):
			if j == 0:
				perm = [0,1,6,5,3,4,2]
			if j == 1:
				perm = [0,6,5,2,4,3,1]
			elif j == 2:
				perm = [0,5,6,1,2,4,3]

			print("Player {}, preference order {}".format(j, perm))
			for i in range(6):
				eq = [0] * 7
				eq[perm[i]] = -1
				eq[perm[i+1]] = 1
				true_combs_base[j].append(eq)
				good_combs[j].add(tuple(eq))
				anti_eq = reverse_comb(eq)
				evil_combs[j].add(tuple(anti_eq))



		running_ind = 0
		failed_run = False

		stage = ""

		firstTime = 0
		interrupt = False
		while not interrupt:
			votes = {}
			critical_level = {}

			begin_length = len(allocs)

			valuations = {0: [], 1: [], 2:[]}

			#for player in range(players):
			#	valuations[player] = generate_valuation(true_combs_base[player])

			bad_combs = {0: set([]), 1: set([]), 2:set([])}
			
			random.shuffle(allocs)


			sampled_allocs = allocs[:1000]

			print("SAMPLED ALLOCS BEFORE FILTER {}".format(len(sampled_allocs)))
			if running_ind % 5 == 0:
				fs_allocs = filter_pareto_dominated(sampled_allocs, true_combs_base, all_combs, good_combs, bad_combs)
				print("SAMPLED ALLOCS AFTER PARETO FILTER {}".format(len(fs_allocs)))
			else:
				fs_allocs = sampled_allocs
			fe_allocs = filter_efx_envious(fs_allocs, true_combs_base, all_combs, good_combs, bad_combs)
			print("SAMPLED ALLOCS AFTER EFX FILTER {}".format(len(fe_allocs)))



			valuations = {0: [], 1: [], 2:[]}

			for player in range(players):
				valuations[player] = generate_valuation(true_combs_base[player])


			start = time.time()

			for alloc in fe_allocs:
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
						anti_key = tuple(reverse_comb(curr_equ))
						if anti_key in evil_combs[pair[0]]:
							continue
						elif is_comb_in_base(anti_key, true_combs_base[pair[0]]):
							evil_combs[pair[0]].add(anti_key)
							continue
						elif tuple([pair[0], tuple(curr_equ)]) in votes:
							votes[tuple([pair[0],tuple(curr_equ)])] += 1
						else:
							votes[tuple([pair[0],tuple(curr_equ)])] = 1
						all_poss_j.append(tuple([pair[0], tuple(curr_equ)]))
				for player, eq in all_poss_j:
					if tuple([player, eq]) not in critical_level:
						critical_level[tuple([player, eq])] = len(all_poss_j)
					else:
						critical_level[tuple([player, eq])] = min(critical_level[tuple([player, eq])], len(all_poss_j))
				if len(all_poss_j) == 0:
					print("Impossible to be EFX envious for alloc {}".format(alloc))
				#random.shuffle(all_poss_j)
			sorted_critical = sorted(critical_level.items(), key=lambda item: item[1]) 


			didAdd = False
			for key, val in sorted_critical:
				if val > 1:
					break
				if tuple(key[1]) in good_combs[key[0]]:
					continue
				anti_key = tuple(reverse_comb(key[1]))
				if tuple(anti_key) in evil_combs[key[0]]:
					print("Critical EFX constraint can not be added. Consider Pareto domination?")
					import pdb
					pdb.set_trace()
					continue
				elif is_comb_in_base(anti_key, true_combs_base[key[0]]):
					evil_combs[player].add(anti_key)
					print("Critical EFX constraint can not be added. Consider Pareto domination?")
					import pdb
					pdb.set_trace()
					continue
				else:
					valuations= generate_valuation(true_combs_base[key[0]] + [tuple(key[1])])
					if valuations is None:
						import pdb
						pdb.set_trace()

					print("Adding critical constraint {}".format(key))

					good_combs[key[0]].add(tuple(key[1]))
					true_combs_base[key[0]].append(tuple(key[1]))
					didAdd = True
					break

			#print(sorted_votes)
			f_votes = {}

			if not didAdd:


				for key, val in critical_level.items():
					player, eq = key
					anti_eq = tuple(reverse_comb(eq))
					if anti_eq in evil_combs[player]:
						continue
					elif is_comb_in_base(anti_eq, true_combs_base[player]):
						evil_combs[player].add(anti_eq)
					else:
						f_votes[key] = val

				sorted_votes = sorted(f_votes.items(), key=lambda item: item[1]) 
				count_cand = 0
				candid = []
				for key, val in sorted_votes:
					if count_cand >= 20:
						break 
					if tuple(key[1]) in good_combs[key[0]]:
						continue
					anti_key = tuple(reverse_comb(key[1]))
					if tuple(anti_key) in evil_combs[key[0]]:
						continue
					elif is_comb_in_base(anti_key, true_combs_base[key[0]]):
						evil_combs[player].add(anti_key)
					else:
						candid.append([key, val])
						count_cand += 1


				min_val = 1000 * 1000
				min_arg = []
				for key, val in candid:
					tcb = copy(true_combs_base[key[0]] + [key[1]])
					bad_val = autocorr(f_votes.keys(), tcb, key[0])
					print("For eq {} critical_val = {}, bad_val = {}".format(key, val, bad_val))
					if bad_val == 0:
						min_arg = key
						break
					else:
						if val * bad_val < min_val:
							min_val = val * bad_val
							min_arg = key

				print("CHOSE {} FOR THE NEXT ROUND".format(min_arg))
				if min_arg == []:
					interrupt = True
					break
				good_combs[min_arg[0]].add(tuple(min_arg[1]))
				true_combs_base[min_arg[0]].append(tuple(min_arg[1]))
			allocs = copy(fe_allocs + allocs[1000:])

			end_length = len(allocs)

			if end_length < 60 and firstTime == 0:
				firstTime = 1
				print("true_combs_base = {}".format(true_combs_base))
				print("allocs = {}".format(allocs))
				print("good_combs = {}".format(good_combs))
				print("evil_combs = {}".format(evil_combs))

			elif end_length < 40 and firstTime < 2:
				firstTime = 2
				print("true_combs_base = {}".format(true_combs_base))
				print("allocs = {}".format(allocs))
				print("good_combs = {}".format(good_combs))
				print("evil_combs = {}".format(evil_combs))


			#print("COVERED {}/{} ALLOCATIONS".format(players**items - len(allocs), players**items))
			running_ind += 1
			const_num = 0
			for player in range(players):
				const_num += len(true_combs_base[player])
			

			print("ITEMS: {}, STAGE: {}, ATTEMPT {}, COMBINATION NUM {}, CONSTRAINT NUMBER {}, GOOD+EVIL = {}, F_VOTES = {}, ALLOCS = {}".format(items, stage, random_try,running_ind, const_num, sum([len(good_combs[player])+len(evil_combs[player]) for player in range(3)]), len(f_votes), len(allocs)))



			if len(allocs) == 0:
				valuations = {0: [], 1: [], 2:[]}

				for player in range(players):
					valuations[player] = generate_valuation(true_combs_base[player])

				print(valuations)
				print("GREAT SUCCESS")
				import pdb
				pdb.set_trace()
		valuations = {0: [], 1: [], 2:[]}

		for player in range(players):
			valuations[player] = generate_valuation(true_combs_base[player])

		print(valuations)
