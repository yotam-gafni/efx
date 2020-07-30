import random
from itertools import product, combinations, permutations
from copy import copy, deepcopy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import pickle
import time

import networkx as nx


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

def prepare_pd_for_allocs(allocs, player, ptrue_combs_base, all_combs, pgood_combs, pbad_combs):
	pd_for_allocs = {}

	all_zeros = [0 for j in range(items)]

	running_ind = 0
	how_many = 0


	bad_combs = {0: set([]), 1: set([]), 2:set([])}

	for alloc in allocs:
		pd_for_alloc = []
		for comb in  all_combs:
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

		pd_for_allocs[tuple(alloc)] = set(pd_for_alloc)

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


	max_stop = 0
	max_conf = {}

	all_comb1 = [list(elem) for elem in permutations([2,3,4,5])]
	all_comb2 = [list(elem) for elem in permutations([1,3,4,5])]
	all_comb3 = [list(elem) for elem in permutations([1,2,4,5])]

	perm = [0,1,2,3,4,5]

	running_ind = 0
	#all_eqs = presets(perm)
	infile = open("eqs_6", "rb")
	all_eqs = pickle.load(infile)

	"""efx_by_eqconf_base = []

	allocs = copy(all_combs)

	running_ind = 0
	for eqconf in all_eqs:
		running_ind += 1
		print("Building efx mapping for equation conf {}".format(running_ind))
		ptrue_combs_base = []

		pgood_combs = set([])
		pevil_combs = set([])

		for j in range(items):
			unit_vector = [0] * 6
			unit_vector[j] = -1
			ptrue_combs_base.append(unit_vector)
			pgood_combs.add(tuple(unit_vector))
			anti_v = reverse_comb(unit_vector)
			pevil_combs.add(tuple(anti_v))
		
		for i in range(5):
			eq = [0] * 6
			eq[perm[i]] = -1
			eq[perm[i+1]] = 1
			ptrue_combs_base.append(eq)
			pgood_combs.add(tuple(eq))
			anti_eq = reverse_comb(eq)
			pevil_combs.add(tuple(anti_eq))
		
		for eq in eqconf:
			anti_eq = reverse_comb(eq)
			ptrue_combs_base.append(eq)
			pgood_combs.add(tuple(eq))
			anti_eq = reverse_comb(eq)
			pevil_combs.add(tuple(anti_eq))



		efx_by_eqconf_base.append(set(partial_filter_efx_envious(allocs, 0, ptrue_combs_base, all_combs, pgood_combs, pevil_combs)))"""


	#outfile = open("efx_by_eqs_6", "wb")
	#pickle.dump(efx_by_eqconf_base,outfile)

	infile = open("efx_by_eqs_6", "rb")
	efx_by_eqconf_base = pickle.load(infile)

	"""pd_for_efx_by_eqconf_base = []
	running_ind = 0
	for i in range(50):
		running_ind += 1
		print("Building PD for {}".format(running_ind))
		eqconf = all_eqs[i]
		allocs = efx_by_eqconf_base[i]
		
		ptrue_combs_base = []

		pgood_combs = set([])
		pevil_combs = set([])

		for j in range(items):
			unit_vector = [0] * 6
			unit_vector[j] = -1
			ptrue_combs_base.append(unit_vector)
			pgood_combs.add(tuple(unit_vector))
			anti_v = reverse_comb(unit_vector)
			pevil_combs.add(tuple(anti_v))
		
		for i in range(5):
			eq = [0] * 6
			eq[perm[i]] = -1
			eq[perm[i+1]] = 1
			ptrue_combs_base.append(eq)
			pgood_combs.add(tuple(eq))
			anti_eq = reverse_comb(eq)
			pevil_combs.add(tuple(anti_eq))
		
		for eq in eqconf:
			anti_eq = reverse_comb(eq)
			ptrue_combs_base.append(eq)
			pgood_combs.add(tuple(eq))
			anti_eq = reverse_comb(eq)
			pevil_combs.add(tuple(anti_eq))


		pd_for_efx_by_eqconf_base.append(prepare_pd_for_allocs(allocs, 0, ptrue_combs_base, all_combs, pgood_combs, pevil_combs))
		"""
	

	#outfile = open("part_pd_by_eqs_6", "wb")
	#pickle.dump(pd_for_efx_by_eqconf_base[:50],outfile)


	infile = open("part_pd_by_eqs_6", "rb")
	pd_for_efx_by_eqconf_base = pickle.load(infile)


	efx_by_eqconf = {0: [], 1: [], 2:[]}
	for eqconf in efx_by_eqconf_base:
		efx_by_eqconf[0].append(copy(eqconf))
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

		efx_by_eqconf[1].append(set(eqconf1))
		efx_by_eqconf[2].append(set(eqconf2))


	pd_for_efx_by_eqconf = {0: [], 1: [], 2: []}

	for alloc_to_pd in pd_for_efx_by_eqconf_base:
		pd_for_efx_by_eqconf[0].append(copy(alloc_to_pd))
		new_alloc_to_pd1 = {}
		new_alloc_to_pd2 = {}

		for alloc, pd_allocs in alloc_to_pd.items():
			new_alloc = []
			for i in range(len(alloc)):
				if alloc[i] == 0:
					new_alloc.append(1)
				elif alloc[i] == 1:
					new_alloc.append(0)
				else:
					new_alloc.append(alloc[i])
			new_pd_allocs = []
			for pda in pd_allocs:
				new_pda = []
				for i in range(len(pda)):
					if pda[i] == 0:
						new_pda.append(1)
					elif pda[i] == 1:
						new_pda.append(0)
					else:
						new_pda.append(pda[i])
				new_pd_allocs.append(tuple(new_pda))
			new_alloc_to_pd1[tuple(new_alloc)] = set(new_pd_allocs)

		for alloc, pd_allocs in alloc_to_pd.items():
			new_alloc = []
			for i in range(len(alloc)):
				if alloc[i] == 0:
					new_alloc.append(2)
				elif alloc[i] == 2:
					new_alloc.append(0)
				else:
					new_alloc.append(alloc[i])
			new_pd_allocs = []
			for pda in pd_allocs:
				new_pda = []
				for i in range(len(pda)):
					if pda[i] == 0:
						new_pda.append(2)
					elif pda[i] == 2:
						new_pda.append(0)
					else:
						new_pda.append(pda[i])
				new_pd_allocs.append(tuple(new_pda))
			new_alloc_to_pd2[tuple(new_alloc)] = set(new_pd_allocs)

		pd_for_efx_by_eqconf[1].append(new_alloc_to_pd1)
		pd_for_efx_by_eqconf[2].append(new_alloc_to_pd2)

	running_ind = 0
	success_ind = 0

	for i1 in range(50):
		for i2 in range(50):
			running_ind += 1
			eq_set1 = all_eqs[i1]
			eq_set2 = all_eqs[i2]
			preferences = []

			for j in range(3):
				preferences.append(copy(perm))

			true_combs_base = {0: [], 1: [], 2: []}

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


			for j in range(3):
				perm = preferences[j]

				#print("Player {}, preference order {}".format(j, perm))
				for i in range(5):
					eq = [0] * 6
					eq[perm[i]] = -1
					eq[perm[i+1]] = 1
					true_combs_base[j].append(eq)
					good_combs[j].add(tuple(eq))
					anti_eq = reverse_comb(eq)
					evil_combs[j].add(tuple(anti_eq))


			for eq in eq_set1:
				anti_eq = reverse_comb(eq)
				true_combs_base[0].append(eq)
				good_combs[0].add(tuple(eq))
				anti_eq = reverse_comb(eq)
				evil_combs[0].add(tuple(anti_eq))	


			for eq in eq_set2:
				anti_eq = reverse_comb(eq)
				true_combs_base[1].append(eq)
				good_combs[1].add(tuple(eq))
				anti_eq = reverse_comb(eq)
				evil_combs[1].add(tuple(anti_eq))	



			allocs = list(efx_by_eqconf[0][i1].intersection(efx_by_eqconf[1][i2]))
			if running_ind % 2000 == 0:
				import pdb
				pdb.set_trace()

			"""G = nx.DiGraph()
			for i in range(6):
				src = tuple([i])
				for j in range(6):
					if i != j:
						dest = [i,j]
						dest.sort()
						G.add_edge(src, tuple(dest))
					for k in range(6):
						dest2 = [i,j,k]
						if len(set(dest2)) == 3:
							dest2.sort()
							G.add_edge(tuple(dest), tuple(dest2))

			src_dst = []
			for i in range(6):
				for j in range(i+1, 6):
					src_dst.append(tuple([tuple([j]), tuple([i])]))
			for src, dst in src_dst:
				G.add_edge(src, dst)
				for i in range(6):
					if i not in src and i not in dst:
						new_src = [i] + list(src)
						new_dst = [i] + list(dst)
						new_src.sort()
						new_dst.sort()
						G.add_edge(tuple(new_src), tuple(new_dst))
						for j in range(6):
							if j not in new_src and j not in new_dst:
								nn_src = [j] + new_src
								nn_dst = [j] + new_dst
								nn_src.sort()
								nn_dst.sort()
								G.add_edge(tuple(nn_src), tuple(nn_dst))


			avail_graphs = [G]
			alloc_ind = 0"""
			for alloc in allocs:
				alloc_ind += 1
				print("Going over alloc {} number {}, available graphs: {}".format(alloc, alloc_ind, len(avail_graphs)))
				src_dst_pairs = []
				if 2 in alloc:
					items_by_agent = [[],[],[]]
					for i in range(6):
						elem = alloc[i]
						items_by_agent[elem].append(i)
					for elem in items_by_agent[0]:
						iba = copy(items_by_agent[0])
						iba.remove(elem)
						if iba:
							src_dst_pairs.append(tuple([tuple(items_by_agent[2]), tuple(iba)]))
					
					for elem in items_by_agent[1]:
						iba = copy(items_by_agent[1])
						iba.remove(elem)
						if iba:
							src_dst_pairs.append(tuple([tuple(items_by_agent[2]), tuple(iba)]))

					# (2,2,2) must have EFX envy, it can not be a PD relation
					if not set([len(items_by_agent[0]), len(items_by_agent[1]), len(items_by_agent[2])]) == set([2]):
						all_pd = pd_for_efx_by_eqconf[0][i1][alloc].intersection(pd_for_efx_by_eqconf[1][i2][alloc])
						ibaset = set(items_by_agent[2])

						for pd_cand in all_pd:
							iba_pd = [[],[],[]]
							for i in range(6):
								elem = pd_cand[i]
								iba_pd[elem].append(i)

							if iba_pd != items_by_agent:
								if2set = set(iba_pd[2])
								if not if2set.issubset(ibaset):
									src = ibaset.difference(if2set)
									dst = if2set.difference(ibaset)
									src_dst_pairs.append(tuple([tuple(src), tuple(dst)]))

					#new_avail_graphs = []
					#set_of_edges = set([])
					#print("Available src-dst pairs: {}, number {}".format(src_dst_pairs, len(src_dst_pairs)))

					if len(src_dst_pairs) == 0:
						success_ind += 1
						break
					"""for src, dst in src_dst_pairs:
						for G in avail_graphs:
							aliG = deepcopy(G)
							aliG.add_edge(src, dst)
							if max(len(src), len(dst)) < 3:
								for i in range(6):
									if i not in src and i not in dst:
										new_src = [i] + list(src)
										new_dst = [i] + list(dst)
										new_src.sort()
										new_dst.sort()
										aliG.add_edge(tuple(new_src), tuple(new_dst))
										if max(len(new_src), len(new_dst)) < 3:
											for j in range(6):
												if j not in new_src and j not in new_dst:
													nn_src = [j] + new_src
													nn_dst = [j] + new_dst
													nn_src.sort()
													nn_dst.sort()
													aliG.add_edge(tuple(nn_src), tuple(nn_dst))
							try:
								ret = nx.find_cycle(aliG)
								#print("Graph contains a contradiction for src {} dst {}".format(src, dst))
							except Exception as e:
								if tuple(aliG.edges()) not in set_of_edges:
									new_avail_graphs.append(aliG)
									set_of_edges.add(tuple(aliG.edges()))
								#else:
									#print("Found a dup graph")"""
				#else:
				#	new_avail_graphs = avail_graphs

				"""if len(new_avail_graphs) == 0:
					print("Derived a contradiction, moving on")
					import pdb
					pdb.set_trace()
					avail_graphs = new_avail_graphs
					break
				avail_graphs = new_avail_graphs"""




			"""items_appear = [0] * 6
			for alloc in allocs:
				items_by_agent = [[],[],[]]
				for i in range(6):
					elem = alloc[i]
					items_by_agent[elem].append(i)
				if set([len(items_by_agent[0]), len(items_by_agent[1]), len(items_by_agent[2])]) == set([2]):
					items_appear[items_by_agent[2][0]] = 1
					items_appear[items_by_agent[2][1]] = 1

				elif len(items_by_agent[2]) == 1:
					all_pd = pd_for_efx_by_eqconf[0][i1][alloc].intersection(pd_for_efx_by_eqconf[1][i2][alloc])
					fap = list(filter(lambda x: 2 in x, all_pd))
					if len(fap) < 2:
						items_appear[items_by_agent[2][0]] = 1


			if set(items_appear) == set([1]):
				print("Running ind passed: {}".format(running_ind))
				success_ind += 1

			else: 
				print("Runnning ind needs more inspection: {}".format(running_ind))"""

			if len(avail_graphs) > 0:
				print("WOOOO")
				import pdb
				pdb.set_trace()
			else:
				print("Went over running ind {}, success {}".format(running_ind))
				import pdb
				pdb.set_trace()

	print("Success percent: {}".format(success_ind / running_ind))



