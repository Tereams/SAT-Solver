import random
from collections import Counter
from read_cnf import read_dimacs

def unit_clause(formula, counter):
    prop=0
    max_count=-1
    for clause in formula:
        if len(clause) == 1:
            if counter[clause[0]]>max_count:
                prop=clause[0]
                max_count=counter[clause[0]]
    return prop

def simplify_formula(formula, counter, proposition, value):
    simplified = []
    for clause in formula:
        truth_value=False
        new_clause=[]
        for lit in clause:
            if abs(lit) == proposition:
                truth_value= truth_value or ((lit < 0) ^ value)
                counter[lit]-=1
            else:
                new_clause.append(lit)
        if truth_value:
            for lit in new_clause:
                counter[lit]-=1
        else:
            if len(new_clause)==0:
                return None
            else:
                simplified.append(new_clause)             
    return simplified

def dpll(formula):
    ini_counter=improved_counter(formula)
    stack = [(formula, {}, ini_counter)]
    count=0
    while stack:
        count+=1
        current_formula, assignment, counter = stack.pop()

        if current_formula == []:
            print(count)
            return True, assignment

        prop = unit_clause(current_formula, counter)
        if prop !=0:
            value = True if prop > 0 else False
            prop = abs(prop)
            new_counter=counter.copy()
            simplified = simplify_formula(current_formula, new_counter, prop, value)
            if simplified is not None:
                stack.append((simplified, {**assignment, prop: value}, new_counter))

        else:
            prop = improved_heuristic(current_formula, counter)
            value = True if prop > 0 else False
            prop = abs(prop)
            for val in (not value, value):
                new_counter=counter.copy()
                simplified = simplify_formula(current_formula, new_counter, prop, val)
                if simplified is not None:
                    stack.append((simplified, {**assignment, prop: val}, new_counter))
    
    return False, {}

def random_choice_counter():
    pass
# Random-choice heuristic
def random_choice_heuristic(formula):
    literals = [lit for clause in formula for lit in clause]
    proposition = abs(random.choice(literals))
    value = random.choice([True, False])
    return proposition, value

def improved_counter(formula):
    count = Counter(lit for clause in formula for lit in clause)
    return count
def improved_heuristic(formula, count):
    if not count:
        return random_choice_heuristic(formula)    
    proposition = max(count, key=count.get)
    return proposition


def generate_3sat(n: int, l: int):
    """Generate random 3-SAT formulas."""
    clauses = []
    for _ in range(l):
        clause = random.sample(range(1, n + 1), 3)
        clause = [lit if random.random() > 0.5 else -lit for lit in clause]
        clauses.append(clause)
    return clauses

# Example usage
if __name__ == "__main__":

    num_vars, clauses = read_dimacs("einstein_riddle_real_true.cnf")

    test_formula = [
        [1, -3, 4],
        [-1, 1],
        [-2, -3],
        [3, -4]
    ]

    print("Improved Heuristic:")
    result, assignment = dpll(clauses, improved_heuristic)
    sorted_dict = {key: assignment[key] for key in sorted(assignment.keys())}
    count = sum(value for value in assignment.values())
    print("Satisfiable:", result, "Assignment:", sorted_dict, "Count:", count)
