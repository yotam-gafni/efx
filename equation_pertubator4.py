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
		if con_string == "":
			import pdb
			pdb.set_trace()
		else:
			constraints.append(con_string + " < 0")

	opt_goal = "5"

	constraint_string = "{" + ",".join(constraints) + "}"

	variable_string += ",".join(variables) + "}"

	lp_string = "Quiet[Maximize[" + opt_goal + ", " + constraint_string + "," + variable_string + "]]"

	is_feasible = session.evaluate(wlexpr(lp_string))

	valuation = []

	try:
		for item in range(items):
			if type(is_feasible[1][item][1]) == int:
				valuation.append(is_feasible[1][item][1])
			else:
				valuation.append(is_feasible[1][item][1][0] / is_feasible[1][item][1][1])

		return valuation
	except Exception as e:
		return None


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

items = 6
all_combs = [item for item in product([i for i in range(players)], repeat=items)]
all_equations = [item for item in product([-1,0,1], repeat=items)]


random.shuffle(all_combs)

efx_combs = []


def serialize(valuations):
	return tuple([tuple(valuations[0]), tuple(valuations[1]), tuple(valuations[2])])

def test_val(valuations):
	efx_combs = []
	for comb in all_combs:
		all_poss_j = []
		isAlreadyJealous = False
		for pair in all_pairs:
			side1_items = []
			side2_items = []
			for i in range(len(comb)):
				if comb[i] == pair[0]:
					side1_items.append(i)
				elif comb[i] == pair[1]:
					side2_items.append(i)
			val_side1 = 0
			for side1_item in side1_items:
				val_side1 += valuations[pair[0]][side1_item]
			for j in range(len(side2_items)):
				val_side2 = 0
				for side2_item in (side2_items[:j] + side2_items[j+1:]):
					val_side2 += valuations[pair[0]][side2_item]

				if val_side2 > val_side1:
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

	old_efx_valuations = copy(efx_valuations)

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
		efx_valuations = new_efx_valuations
		if efx_valuations == []:
			print("REALLY??")
			import pdb
			pdb.set_trace()

	print("FINAL LEN: {} for valuation {}".format(len(efx_valuations), valuations))
	return len(efx_valuations)

def build_equation_dict(valuations, contra_eq = None):

	eq_dict = dict()

	all_zeros = [0 for j in range(items)]

	for i in range(players):
		eq_dict[i] = []
		for j in range(items):
			unit_vector = copy(all_zeros)
			unit_vector[j] = -1
			eq_dict[i].append(unit_vector)

	if contra_eq:
		random.shuffle(contra_eq)
		for player, eq in contra_eq:
			anti_eq = reverse_comb(eq)
			if not is_comb_in_base(anti_eq, eq_dict[player]):
				eq_dict[player].append(eq)
				break

	count_stuff = 0
	for player in range(players):
		print("BUILDING FOR PLAYER {}".format(player))

		curr_equations = copy(all_equations)
		random.shuffle(curr_equations)
		for eq in curr_equations:
			first_non_zero = 0
			for item in eq:
				if eq[item] != 0:
					first_non_zero = eq[item]
					break
			if first_non_zero == 1 and -1 in eq:
				sum_val = 0
				for item in range(items):
					sum_val += valuations[player][item] * eq[item]


				anti_comb = reverse_comb(eq)
				count_stuff += 2
				if not is_comb_in_base(eq, eq_dict[player]) and not is_comb_in_base(anti_comb, eq_dict[player]):
					flip_choice = False
					if random.random() < 1/50:
						flip_choice = True

					if (sum_val < 0 and not flip_choice) or (sum_val > 0 and flip_choice):
						eq_dict[player].append(eq)
					else:
						eq_dict[player].append(anti_comb)

	print("COUNT STUFF: {}".format(count_stuff))
	return eq_dict

def pertube(base_valuations, level, all_contra_eq = None):
	for random_try in range(10000):
		print("BEFORE")
		eq_dict = build_equation_dict(base_valuations, all_contra_eq)
		print("AFTER")
		val = {0: [], 1: [], 2:[]}

		shouldTest = True

		for player in range(players):
			val[player] = generate_valuation(eq_dict[player])
			if val[player] == None:
				print("Invalid valuation, moving on with random_try={}".format(random_try))
				shouldTest = False
				break
		if shouldTest:
			res = test_val(val)
			if res <= level:
				return val, res
	return None, None


def find_evil_comb(valuations):	



	all_zeros = [0 for j in range(items)]


	part_val = [22,15,10]

	for comb in all_combs:
		all_poss_j = []
		isAlreadyJealous = False
		for pair in all_pairs:
			side1_items = []
			side2_items = []
			for i in range(len(comb)):
				if comb[i] == pair[0]:
					side1_items.append(i)
				elif comb[i] == pair[1]:
					side2_items.append(i)
			val_side1 = 0
			for side1_item in side1_items:
				val_side1 += valuations[pair[0]][side1_item]
			for j in range(len(side2_items)):
				val_side2 = 0
				for side2_item in (side2_items[:j] + side2_items[j+1:]):
					val_side2 += valuations[pair[0]][side2_item]

				if val_side2 > val_side1:
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
	#print(efx_combs)

	old_efx_valuations = copy(efx_valuations)

	print("All EFX Valuations: {}".format(old_efx_valuations))
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
			#else:
			#	print("EFX comb {} with values {} superseded by {} due to combination {}".format(e_comb, e_val, new_val, comb))
		efx_valuations = new_efx_valuations
		if efx_valuations == []:
			print("REALLY??")
			import pdb
			pdb.set_trace()
	print("EFX+PO Valuations: {}".format(efx_valuations))

	return efx_valuations

def choose_contra_equation(evil_comb):
	all_zeros = [0 for j in range(items)]

	all_poss_j = []
	for pair in all_pairs:
		side1_items = []
		side2_items = []
		equ = copy(all_zeros)
		for i in range(len(evil_comb)):
			if evil_comb[i] == pair[0]:
				side1_items.append(i)
				equ[i] = 1
			elif evil_comb[i] == pair[1]:
				side2_items.append(i)
				equ[i] = -1

		for j in side2_items:
			curr_equ = copy(equ)
			curr_equ[j] = 0
			if sum(curr_equ) == 0 and len(set(curr_equ)) == 1:
				continue
			all_poss_j.append(tuple([pair[0], curr_equ]))

	return all_poss_j
#base_valuations = {0: [1, 5.1, 5, 1, 3], 1: [1, 0.375, 1.3, 0.125, 0.125], 2: [1, 5, 4.5, 3, 1]}
#base_valuations = {0: [1, 17, 13, 4.5, 6.5], 1: [1, 0.4107142857142857, 1.4017857142857142, 0.13392857142857142, 0.20535714285714285], 2: [1, 5.75, 5.25, 3.75, 1.25]}
#base_valuations = {0: [1, 5.1, 5, 1, 3,0.2], 1: [1, 0.375, 1.3, 0.125, 0.125, 0], 2: [1, 5, 4.5, 3, 1, 0]}
#base_valuations = {0: [1.02, 5.01, 1, 1, 3,0.009,0.009,0,0.01], 1: [1, 0.375, 1.15, 0.125, 0.125,0,0,0,0], 2: [1, 5.01, 3, 3, 1.1,0.01,0.1,0.01,0]}
#base_valuations = {0: [1, 6.552083333333333, 5.78125, 0.6458333333333334, 3.8958333333333335, 0.4791666666666667], 1: [1, 0.04201388888888889, 1.8125, 0.3861111111111111, 0.37569444444444444, 0.40520833333333334], 2: [1, 9.458333333333334, 8.791666666666666, 5.666666666666667, 2.8333333333333335, 0.16666666666666666]}
#base_valuations = {0: [1, 7.302083333333333, 6.46875, 0.7708333333333334, 4.333333333333333, 0.7291666666666666], 1: [1, 0.18055555555555555, 1.7951388888888888, 0.3229166666666667, 0.28125, 0.4548611111111111], 2: [1, 6.927083333333333, 6.354166666666667, 3.3229166666666665, 2.6875, 0.11458333333333333]}
#base_valuations = {0: [1, 30, 23.75, 6.75, 11, 4], 1: [1, 0.06160714285714286, 1.9995535714285715, 0.09285714285714286, 0.7651785714285714, 0.11071428571428571], 2: [1, 4.091666666666667, 3.9125, 0.8625, 1.4333333333333333, 1.0541666666666667]}
#base_valuations = {0: [1, 6.984375, 6.078125, 2.859375, 2.703125, 1.453125], 1: [1, 0.06220238095238095, 1.974702380952381, 0.18720238095238095, 0.5511904761904762, 0.2199404761904762], 2: [1, 4.64375, 4.8375, 0.95, 1.69375, 1.6125]}
#base_valuations = {0: [1, 8.9375, 7.875, 3.5625, 3.4375, 1.4375], 1: [1, 0.8145833333333333, 3.221875, 0.68125, 0.38125, 0.5354166666666667], 2: [1, 5.041666666666667, 4.75, 0.5833333333333334, 1.6458333333333333, 1.8125]}
#base_valuations = {0: [1, 8.5625, 7.5, 3.45, 3.178125, 1.36875, 0.003125], 1: [1, 0.5254464285714285, 2.3457589285714286, 0.36964285714285716, 0.3380208333333333, 0.22686011904761905, 0.023809523809523808], 2: [1, 8.029761904761905, 7.261904761904762, 1.0982142857142858, 2.824404761904762, 2.7708333333333335, 0.11607142857142858]}
#base_valuations = {0: [1, 5.559895833333333, 6.105729166666666, 0.2557291666666667, 2.0494791666666665, 1.3708333333333333, 1.5536458333333334], 1: [1, 5.536147186147186, 6.612337662337662, 1.8571428571428572, 1.3417748917748917, 0.3372294372294372, 0.01103896103896104], 2: [1, 5.801897321428571, 3.7631138392857144, 0.012834821428571428, 2.4679129464285716, 2.3016183035714284, 0.4330357142857143]}
#base_valuations = {0: [1, 5.559895833333333, 6.105729166666666, 0.2557291666666667, 2.0494791666666665, 1.3708333333333333, 1.5536458333333334], 1: [1, 5.536147186147186, 6.612337662337662, 1.8571428571428572, 1.3417748917748917, 1.3372294372294372, 0.01103896103896104], 2: [1, 5.801897321428571, 3.7631138392857144, 0.012834821428571428, 2.4679129464285716, 2.3016183035714284, 0.4330357142857143]}
#base_valuations = {0: [1, 6.520833333333333, 7.271527777777778, 1.2416666666666667, 1.8125, 1.054861111111111, 2.290277777777778], 1: [1, 6.1953125, 7.5390625, 2.2265625, 1.84375, 0.125, 0.2265625], 2: [1, 8.895833333333334, 6.1875, 0.026041666666666668, 2.75, 2.4322916666666665, 0.40625]}
#base_valuations = {0: [1, 6.520833333333333, 7.271527777777778, 1.2416666666666667, 1.8125, 1.054861111111111, 2.290277777777778, 0.3], 1: [1, 6.1953125, 7.5390625, 2.2265625, 1.84375, 0.125, 0.2265625, 0], 2: [1, 8.895833333333334, 6.1875, 0.026041666666666668, 2.75, 2.4322916666666665, 0.40625, 0]}
#base_valuations = {0: [1, 0.11904761904761904, 0.8095238095238095, 0.7619047619047619, 1.7083333333333333, 1.9107142857142858], 1: [1, 1.0342261904761905, 0.3236276455026455, 0.19773478835978836, 0.5982473544973544, 0.25329034391534394], 2: [1, 1.13125, 2.08125, 1.825, 1.675, 1.575]}
base_valuations = {0: [1, 0.7302556818181818, 1.0367897727272728, 0.18451704545454545, 1.5535511363636363, 1.576278409090909], 1: [1, 0.6617897727272727, 0.5433238636363636, 0.36477272727272725, 0.6039772727272728, 0.25866477272727273], 2: [1, 0.16666666666666666, 1.578125, 1.5572916666666667, 0.7395833333333334, 0.84375]}
level = 1


while base_valuations != None:
	values, evil_comb = find_evil_comb(base_valuations)[0]
	contra_eq = choose_contra_equation(evil_comb)
	base_valuations, level = pertube(base_valuations, level, contra_eq)