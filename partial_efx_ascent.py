import random

players = 3
items = 7

valuations = [[],[],[]]

assignment = [[],[],[],[i for i in range(7)]]

random.seed(11)

for i in range(items):
	valuations[0].append(random.random())
	valuations[1].append(random.random())
	valuations[2].append(random.random())

def lex_superior(assign1, assign2):
	if assign1 == assign2:
		return False
	for i in range(3):
		old_value = sum([valuations[i][k] for k in assign2[i]])
		new_value = sum([valuations[i][k] for k in assign1[i]])
		if new_value < old_value:
			return False

	return True

def is_efx(assignment):
	for i in range(3):
		own_value = sum([valuations[i][k] for k in assignment[i]])
		for j in range(3):
			if j != i:
				other_items = [valuations[i][k] for k in assignment[j]]
				for item_ind in range(len(other_items)):
					alt_items = other_items[:item_ind] + other_items[item_ind + 1:]
					other_value = sum(alt_items)
					if own_value < other_value:
						return False
	return True

def is_full_efx(assignment):
	return is_efx(assignment) and assignment[3] == []

while not is_full_efx(assignment):
	eg = build_envy_graph(assignment)
	cg = build_champions_graph(assignment, assignment[3][0])
	if section_2_conditions:
		new_assignment = section2_process(assignment)
	elif section_3_conditions:
		new_assignment = section3_process(assignment)
	elif section_4_conditions:
		new_assignment = section4_process(assignment)

	if not is_efx(new_assignment):
		print("WTF NOT EFX")

	if not lex_superior(new_assignment, assignment):
		print("WTF NOT LEX")
