import random
from itertools import product, combinations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()



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

	is_feasible = session.evaluate(wlexpr(lp_string))

	valuation = []

	for item in range(items):
		if type(is_feasible[1][item][1]) == int:
			valuation.append(is_feasible[1][item][1])
		else:
			valuation.append(is_feasible[1][item][1][0] / is_feasible[1][item][1][1])

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



players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

for items in range(10,13):

	all_combs = [item for item in product([i for i in range(players)], repeat=items)]

	max_stop = 0
	max_conf = {}

	for random_try in range(1000):
		#print("RANDOM TRY: {}".format(random_try))
		true_combs_base = dict()

		all_zeros = [0 for j in range(items)]

		for i in range(players):
			true_combs_base[i] = []
			for j in range(items):
				unit_vector = copy(all_zeros)
				unit_vector[j] = -1
				true_combs_base[i].append(unit_vector)


		random.shuffle(all_combs)



		running_ind = 0
		failed_run = False


		for comb in all_combs:
			running_ind += 1
			if running_ind % 1000 == 0:
				print("ATTEMPT {}, COMBINATION NUM {}".format(random_try,running_ind))

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

			if isAlreadyJealous == False:
				for elem in all_poss_j:
					anti_comb = reverse_comb(elem[1])
					if not is_comb_in_base(anti_comb, true_combs_base[elem[0]]):
						#anti_comb = reverse_comb(elem[1])
						true_combs_base[elem[0]].append(elem[1])
						isAlreadyJealous = True
						break

			if isAlreadyJealous == False:
				print("RANDOM TRY: {}, FAILED ON COMBINATION {}/{}, MAX SUCCESS {}/{}".format(random_try,running_ind,players**items,max_stop, players**items))
				break

		if running_ind > players**items / 2:

			random.shuffle(all_combs)
			all_zeros = [0 for j in range(items)]

			efx_combs = []


			for comb in all_combs:
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

				if isAlreadyJealous == False:
					for elem in all_poss_j:
						anti_comb = reverse_comb(elem[1])
						if not is_comb_in_base(anti_comb, true_combs_base[elem[0]]):
							#anti_comb = reverse_comb(elem[1])
							true_combs_base[elem[0]].append(elem[1])
							isAlreadyJealous = True
							break

				if isAlreadyJealous == False:
					efx_combs.append(comb)

			valuations = {0: [], 1: [], 2:[]}

			for player in range(players):
				valuations[player] = generate_valuation(true_combs_base[player])


			efx_valuations = []
			for comb in efx_combs:
				new_val = []
				for player in range(players):
					player_value = 0
					for elem_ind in range(len(comb)):
						if comb[elem_ind] == player:
							player_value += valuations[player][elem_ind]

					new_val.append(player_value)
				efx_valuations.append(new_val)

			print(efx_valuations)


			for comb in all_combs:
				new_val = []
				for player in range(players):
					player_value = 0
					for elem_ind in range(len(comb)):
						if comb[elem_ind] == player:
							player_value += valuations[player][elem_ind]

					new_val.append(player_value)

				new_efx_valuations = []
				for e_val in efx_valuations:
					if not pareto_dominates(new_val, e_val):
						new_efx_valuations.append(e_val)
				efx_valuations = new_efx_valuations
				if efx_valuations == []:
					print("REALLY??")
					import pdb
					pdb.set_trace()
			print(efx_valuations)
			if len(efx_valuations) == 1:
				print("KOOKOO!!")
				print(valuations)


	print("MAX STOP PERCENT: {}".format(max_stop / players**items))
