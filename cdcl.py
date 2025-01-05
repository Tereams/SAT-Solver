class CDCLSolver:
    def __init__(self, clauses, num_vars):
        self.clauses = clauses  # Store all clauses
        self.num_vars = num_vars  # Number of variables
        self.assignment = [None] * (num_vars + 1)  # Variable assignments (1-based indexing)
        self.decision_stack = []  # Decision stack
        self.implication_graph = {}  # Implication graph for conflict analysis

    def is_satisfied(self):
        """Check if all clauses are satisfied"""
        for clause in self.clauses:
            if not any((lit > 0 and self.assignment[lit] == True) or \
                       (lit < 0 and self.assignment[-lit] == False) \
                       for lit in clause):
                return False
        return True

    def pick_branching_variable(self):
        """Pick the next decision variable"""
        for i in range(1, self.num_vars + 1):
            if self.assignment[i] is None:
                return i
        return None

    def unit_propagate(self):
        """Perform unit propagation to assign forced variables"""
        propagated = True
        while propagated:
            propagated = False
            for clause in self.clauses:
                unassigned = [lit for lit in clause if self.assignment[abs(lit)] is None]
                true_lits = [lit for lit in clause if \
                             (lit > 0 and self.assignment[lit] == True) or \
                             (lit < 0 and self.assignment[-lit] == False)]
                
                if len(true_lits) == 0 and len(unassigned) == 1:
                    unit = unassigned[0]
                    value = unit > 0
                    self.assignment[abs(unit)] = value
                    self.decision_stack.append((abs(unit), value))
                    self.implication_graph[abs(unit)] = clause
                    propagated = True

    def backtrack(self):
        """Backtrack to the most recent assignable state"""
        while self.decision_stack:
            var, _ = self.decision_stack.pop()
            self.assignment[var] = None
            if var in self.implication_graph:
                del self.implication_graph[var]
            if var < 0:  # Indicates a decision point
                return

    def analyze_conflict(self):
        """Analyze conflict and generate a learned clause"""
        # For simplicity, return an empty clause indicating unsatisfiability
        return []

    def get_model(self):
        """Return the satisfying assignment if SATISFIABLE"""
        return {i: self.assignment[i] for i in range(1, self.num_vars + 1)}

    def solve(self):
        while True:
            self.unit_propagate()
            if self.is_satisfied():
                return True  # Satisfiable solution found

            conflict = any(
                all((lit > 0 and self.assignment[lit] == False) or \
                    (lit < 0 and self.assignment[-lit] == True) for lit in clause) \
                for clause in self.clauses
            )

            if conflict:
                learned_clause = self.analyze_conflict()
                if not learned_clause:
                    return False  # Unsatisfiable

                self.clauses.append(learned_clause)
                self.backtrack()
            else:
                var = self.pick_branching_variable()
                if var is None:
                    return True  # Satisfiable solution found
                self.assignment[var] = True
                self.decision_stack.append((var, True))

# Example:
# (x1 OR x2) AND (NOT x1 OR x3) AND (NOT x2 OR NOT x3)
clauses = [[1, 2], [-1, 3], [-2, -3]]
num_vars = 3
solver = CDCLSolver(clauses, num_vars)
result = solver.solve()
if result:
    print("SATISFIABLE")
    print("Model:", solver.get_model())
else:
    print("UNSATISFIABLE")
