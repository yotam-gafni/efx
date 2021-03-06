import random
from itertools import product, combinations, permutations
from copy import copy, deepcopy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import pickle
import time

from bitarray import bitarray
from numpy import uint64
from fixedint import UInt64
from ctypes import c_uint64


arrays = []

comb_behavior = {}

global lp_runs
lp_runs = 0


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
					#print("UNFEASIBLE CONSTRAINTS!!!!")
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

	if lp_runs % 10000 == 0:
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




def filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs, bad_combs):
	filtered_allocs = []

	all_zeros = [0 for j in range(items)]
	all_combs_copy = copy(all_combs)

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
				#print("alloc {} is pareto dominated by comb {}, removing".format(alloc, comb))
				foundPD = True
				break

		#print("NOT PD")
		if not foundPD:
			filtered_allocs.append(alloc)
		#print("HOW MANY: {}, FILTERED LENGTH: {}".format(how_many, len(filtered_allocs)))

	return filtered_allocs

def prepare_pd_for_allocs(allocs, player, ptrue_combs_base, all_combs, pgood_combs, pbad_combs, tuple_to_int):
	pd_for_allocs = {}

	all_zeros = [0 for j in range(items)]

	running_ind = 0
	how_many = 0


	bad_combs = {0: set([]), 1: set([]), 2:set([])}

	for alloc in allocs:
		pd_for_alloc = []
		for comb in  all_combs:
			if comb != alloc:
				running_ind += 1
				eq = [0] * 6

				for i in range(items):
					if alloc[i] == 0 and comb[i] != 0:
						eq[i] = 1
					elif comb[i] == 0 and alloc[i] != 0:
						eq[i] = -1

				if sum(eq) == 0 and len(set(eq)) == 1:
					pd_for_alloc.append(tuple(comb))
				elif 1 not in eq:
					pd_for_alloc.append(tuple(comb))
				elif -1 not in eq:
					continue
				
				elif tuple(eq) in pgood_combs:
					pd_for_alloc.append(tuple(comb))

				elif tuple(eq) in pbad_combs:
					continue

				elif is_comb_in_base(eq, ptrue_combs_base):
					pd_for_alloc.append(tuple(comb))
					pgood_combs.add(tuple(eq))
				else:
					pbad_combs.add(tuple(eq))

		pd_for_allocs[tuple_to_int[tuple(alloc)]] = set_to_int(set(pd_for_alloc))

	#if tuple([1,0,2,2,0,2]) in allocs:
	#	import pdb
	#	pdb.set_trace()

	return pd_for_allocs

def filter_efx_envious(allocs, true_combs_base, all_combs, good_combs, bad_combs):
	bad_combs = {0: set([]), 1: set([]), 2:set([])}

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

def partial_filter_efx_envious(allocs, player, ptrue_combs_base, all_combs, pgood_combs, pbad_combs):

	filtered_allocs = []
	for alloc in allocs:
		all_poss_j = []
		for pair in all_pairs:
			if pair[0] == player:
				side1_items = []
				side2_items = []
				equ = [0] * items
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

		isAlreadyJealous = False
		count_ops = 0
		for elem in all_poss_j:
			#anti_comb = reverse_comb(elem[1])
			if tuple(elem[1]) in pgood_combs: 
				#print("alloc {} has eq {} for player {}, and thus envious".format(alloc, elem[1], elem[0]))
				isAlreadyJealous = True
				break
			elif tuple(elem[1]) in pbad_combs:
				continue
			elif is_comb_in_base(tuple(elem[1]), ptrue_combs_base):
				count_ops += 1
				pgood_combs.add(tuple(elem[1]))
				#print("alloc {} has eq {} for player {}, and thus envious".format(alloc, elem[1], elem[0]))
				isAlreadyJealous = True
				break
			else:
				pbad_combs.add(tuple(elem[1]))
				continue
		if isAlreadyJealous == False:
			#print("alloc {} has no current envy, performed {} ops".format(alloc, count_ops))
			filtered_allocs.append(alloc)

	return filtered_allocs



def rearrange_pref(eqs, pref):

	new_eqs = []

	for eq in eqs:
		new_eq = [0] * 6
		for i in range(6):
			new_eq[pref[i]] = eq[i]

		new_eqs.append(new_eq)

	return new_eqs

def set_to_numpy_int_array(s1):
	arr = [0] * 12
	for pos in range(12):
		num = pos*62
		for i in range(62):
			num+= 1
			if num < 729:	
				if num in s1:
					arr[pos] += 2**i

	final_arr = []
	for elem in arr:
		final_arr.append(c_uint64(elem))

	return final_arr

def set_to_int(s1):
	res = 0
	for i in range(729):
		if i in s1:
			res += 2**i

	return res

def set_to_ba(s1):
	res = bitarray()
	for i in range(729):
		res.extend([i in s1])

	return res

def int_to_set(i1):
	s1 = set([])
	for i in range(729):
		if i1 % 2 == 1:
			s1.add(i)
		i1 = int(i1/2)

	return s1

def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b



players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

for items in range(6,7):

	all_combs = [item for item in product([i for i in range(players)], repeat=items)]

	tuple_to_int = {}
	int_to_tuple = {}

	running_ind = 0
	for comb in all_combs:
		tuple_to_int[tuple(comb)] = running_ind
		int_to_tuple[running_ind] = tuple(comb)
		running_ind += 1

	max_stop = 0
	max_conf = {}

	all_comb1 = [list(elem) for elem in permutations([2,3,4,5])]
	all_comb2 = [list(elem) for elem in permutations([1,3,4,5])]
	all_comb3 = [list(elem) for elem in permutations([1,2,4,5])]

	two_power_to_log = {}
	for i in range(729):
		two_power_to_log[2**i] = i

	perm = [0,1,2,3,4,5]
	pref = perm

	running_ind = 0
	#all_eqs = presets(perm)
	infile = open("eqs_6", "rb")
	all_eqs = pickle.load(infile)

	ordinal_eqs = []
	for i in range(5):
		eq = [0] * 6
		eq[pref[i]] = -1
		eq[pref[i+1]] = 1
		ordinal_eqs.append(eq)

	# these are goods
	eq = [0] * 6
	eq[pref[0]] = -1
	ordinal_eqs.append(eq)


	allocs = copy(all_combs)



	infile = open("efx_by_eqs_6", "rb")
	efx_by_eqconf_base = pickle.load(infile)


	infile = open("mmm", "rb")
	pd_for_efx_by_eqconf_base = pickle.load(infile)


	efx_by_eqconf = {0: [], 1: [], 2:[]}
	for eqconf in efx_by_eqconf_base[:50]:
		efx_by_eqconf[0].append(set_to_int(set([tuple_to_int[eq] for eq in eqconf])))
		eqconf1 = []
		eqconf2 = []

		for alloc in eqconf:
			new_alloc = []
			for i in range(len(alloc)):
				if alloc[i] == 0:
					new_alloc.append(1)
				elif alloc[i] == 1:
					new_alloc.append(0)
				else:
					new_alloc.append(alloc[i])
			eqconf1.append(tuple(new_alloc))

		for alloc in eqconf:
			new_alloc = []
			for i in range(len(alloc)):
				if alloc[i] == 0:
					new_alloc.append(2)
				elif alloc[i] == 2:
					new_alloc.append(0)
				else:
					new_alloc.append(alloc[i])
			eqconf2.append(tuple(new_alloc))

		efx_by_eqconf[1].append(set_to_int(set([tuple_to_int[eq] for eq in eqconf1])))
		efx_by_eqconf[2].append(set_to_int(set([tuple_to_int[eq] for eq in eqconf2])))



	pd_for_efx_by_eqconf = {0: [], 1: [], 2: []}

	for alloc_to_pd in pd_for_efx_by_eqconf_base[:50]:
		if alloc_to_pd is not None:
			new_alloc_to_pd0 = {}
			new_alloc_to_pd1 = {}
			new_alloc_to_pd2 = {}

			for alloc_int, pd_allocs in alloc_to_pd.items():
				new_alloc_to_pd0[tuple_to_int[alloc]] = set_to_int(set([tuple_to_int[al] for al in int_to_set(pd_allocs)]))
				alloc = int_to_tuple[alloc_int]
				new_alloc = []
				for i in range(len(alloc)):
					if alloc[i] == 0:
						new_alloc.append(1)
					elif alloc[i] == 1:
						new_alloc.append(0)
					else:
						new_alloc.append(alloc[i])
				new_pd_allocs = []
				for pda in int_to_set(pd_allocs):
					new_pda = []
					for i in range(len(pda)):
						if pda[i] == 0:
							new_pda.append(1)
						elif pda[i] == 1:
							new_pda.append(0)
						else:
							new_pda.append(pda[i])
					new_pd_allocs.append(tuple(new_pda))
				new_alloc_to_pd1[tuple_to_int[tuple(new_alloc)]] = set_to_int(set([tuple_to_int[al] for al in new_pd_allocs]))

			for alloc_int, pd_allocs in alloc_to_pd.items():
				alloc = int_to_tuple[alloc_int]
				new_alloc = []
				for i in range(len(alloc)):
					if alloc[i] == 0:
						new_alloc.append(2)
					elif alloc[i] == 2:
						new_alloc.append(0)
					else:
						new_alloc.append(alloc[i])
				new_pd_allocs = []
				for pda in int_to_set(pd_allocs):
					new_pda = []
					for i in range(len(pda)):
						if pda[i] == 0:
							new_pda.append(2)
						elif pda[i] == 2:
							new_pda.append(0)
						else:
							new_pda.append(pda[i])
					new_pd_allocs.append(tuple(new_pda))
				new_alloc_to_pd2[tuple_to_int[tuple(new_alloc)]] = set_to_int(set([tuple_to_int[al] for al in new_pd_allocs]))

			pd_for_efx_by_eqconf[0].append(new_alloc_to_pd0)
			pd_for_efx_by_eqconf[1].append(new_alloc_to_pd1)
			pd_for_efx_by_eqconf[2].append(new_alloc_to_pd2)
		else:
			pd_for_efx_by_eqconf[0].append(None)
			pd_for_efx_by_eqconf[1].append(None)
			pd_for_efx_by_eqconf[2].append(None)


	running_ind = 0
	start = time.time()
	efx_times = 0
	for i1 in range(50):
		for i2 in range(50):
			if pd_for_efx_by_eqconf[0][i1] is not None and pd_for_efx_by_eqconf[1][i2] is not None:
				efx_start = time.time()
				iebe = efx_by_eqconf[0][i1] & efx_by_eqconf[1][i2]
				efx_end = time.time()
				efx_times += efx_end - efx_start

				iebe_pd = {}
				for i3 in range(50):
					if pd_for_efx_by_eqconf[2][i3] is not None:
						running_ind += 1

						efx_start = time.time()
						allocs_int = iebe & efx_by_eqconf[2][i3]
						efx_end = time.time()
						efx_times += efx_end - efx_start

						failed = False

						for b in bits(allocs_int):
							alloc = two_power_to_log[b]
							if alloc not in iebe_pd:
								#iebe_pd[alloc] = []
								#for i in range(12):
								#iebe_pd[alloc].append(pd_for_efx_by_eqconf[0][i1][alloc][i] & pd_for_efx_by_eqconf[1][i2][alloc][i])
								iebe_pd[alloc] = pd_for_efx_by_eqconf[0][i1][alloc] & pd_for_efx_by_eqconf[1][i2][alloc]

							"""count_elem = 0
							for elem in pd_for_efx_by_eqconf[2][i3][alloc]:
								if elem in iebe_pd[alloc]:
									count_elem += 1
								if count_elem > 1:
									break 
							if count_elem < 2:
								break """
							#if (iebe_pd[alloc] & pd_for_efx_by_eqconf[2][i3][alloc]) == zero:
							"""quit_compare = False
							for i in range(12):
								if (iebe_pd[alloc][i] & pd_for_efx_by_eqconf[2][i3][alloc][i]) != 0:
									quit_compare = True
									break
							if quit_compare:
								continue"""
							#else:
							if (iebe_pd[alloc] & pd_for_efx_by_eqconf[2][i3][alloc]) == 0:
							#if len(iebe_pd[alloc].intersection(pd_for_efx_by_eqconf[2][i3][alloc])) == 0:
								failed = True
								break



						if not failed:
							print("WOOPEE")
							import pdb
							pdb.set_trace()
						else:
							if running_ind % 10000 == 0:
								print("Running ind: {}".format(running_ind))

	end = time.time()

	print("Took {}".format(end - start))
	print("Only EFX took {}".format(efx_times))

