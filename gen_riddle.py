# Python code to generate the DIMACS CNF file for Einstein's riddle

# Define constants
NUM_HOUSES = 5
ATTRIBUTES = ["color", "nationality", "drink", "cigar", "pet"]
VALUES = {
    "color": ["red", "green", "white", "yellow", "blue"],
    "nationality": ["Brit", "Swede", "Dane", "German", "Norwegian"],
    "drink": ["tea", "coffee", "milk", "beer", "water"],
    "cigar": ["PallMall", "Dunhill", "Blends", "Bluemasters", "Prince"],
    "pet": ["fish", "dogs", "birds", "cats", "horse"]
}

# Generate variable IDs
def generate_variable_id(attribute, value, house):
    attr_offset = list(VALUES.keys()).index(attribute) * NUM_HOUSES * len(VALUES[attribute])
    value_offset = VALUES[attribute].index(value) * NUM_HOUSES
    return attr_offset + value_offset + house + 1

# Generate clauses for uniqueness constraints
clauses = []
# Each house has exactly one value for each attribute
for attribute, values in VALUES.items():
    for house in range(NUM_HOUSES):
        # At least one value for each attribute in a house
        clauses.append([generate_variable_id(attribute, value, house) for value in values])
        # No two values for the same attribute in a house
        for i, value1 in enumerate(values):
            for value2 in values[i+1:]:
                clauses.append([
                    -generate_variable_id(attribute, value1, house),
                    -generate_variable_id(attribute, value2, house)
                ])

# Each value appears in exactly one house
for attribute, values in VALUES.items():
    for value in values:
        for house1 in range(NUM_HOUSES):
            for house2 in range(house1+1, NUM_HOUSES):
                clauses.append([
                    -generate_variable_id(attribute, value, house1),
                    -generate_variable_id(attribute, value, house2)
                ])

# Add the hints as clauses
# Hint 1: The Brit lives in the red house
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("nationality", "Brit", house),
        generate_variable_id("color", "red", house)
    ])

# Hint 2: The Swede keeps dogs
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("nationality", "Swede", house),
        generate_variable_id("pet", "dogs", house)
    ])

# Hint 3: The Dane drinks tea
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("nationality", "Dane", house),
        generate_variable_id("drink", "tea", house)
    ])

# Hint 4: The green house is on the left of the white house
for house in range(NUM_HOUSES - 1):
    clauses.append([
        -generate_variable_id("color", "green", house),
        generate_variable_id("color", "white", house + 1)
    ])
clauses.append([
        -generate_variable_id("color", "green", 4)
    ])

# Hint 5: The green house’s owner drinks coffee
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("color", "green", house),
        generate_variable_id("drink", "coffee", house)
    ])

# Hint 6: The person who smokes Pall Mall rears birds
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("cigar", "PallMall", house),
        generate_variable_id("pet", "birds", house)
    ])

# Hint 7: The owner of the yellow house smokes Dunhill
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("color", "yellow", house),
        generate_variable_id("cigar", "Dunhill", house)
    ])

# Hint 8: The man living in the center house drinks milk
clauses.append([
        generate_variable_id("drink", "milk", NUM_HOUSES//2)
    ])

# Hint 9: The Norwegian lives in the first house
clauses.append([
        generate_variable_id("nationality", "Norwegian", 0)
    ])

# Hint 10: The man who smokes Blends lives next to the one who keeps cats
for house in range(1,NUM_HOUSES-1):
    clauses.append([
        -generate_variable_id("cigar", "Blends", house),
        generate_variable_id("pet", "cats", house-1),
        generate_variable_id("pet", "cats", house+1)
    ])
clauses.append([
        -generate_variable_id("cigar", "Blends", 0),
        generate_variable_id("pet", "cats", 1),
    ])
clauses.append([
        -generate_variable_id("cigar", "Blends", 4),
        generate_variable_id("pet", "cats", 3),
    ])

# Hint 11: The man who keeps the horse lives next to the man who smokes Dunhill
for house in range(1,NUM_HOUSES-1):
    clauses.append([
        -generate_variable_id("pet", "horse", house),
        generate_variable_id("cigar", "Dunhill", house-1),
        generate_variable_id("cigar", "Dunhill", house+1)
    ])
clauses.append([
        -generate_variable_id("pet", "horse", 0),
        generate_variable_id("cigar", "Dunhill", 1),
    ])
clauses.append([
        -generate_variable_id("pet", "horse", 4),
        generate_variable_id("cigar", "Dunhill", 3),
    ])

# Hint 12: The owner who smokes Bluemasters drinks beer
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("cigar", "Bluemasters", house),
        generate_variable_id("drink", "beer", house)
    ])

# Hint 13: The German smokes Prince
for house in range(NUM_HOUSES):
    clauses.append([
        -generate_variable_id("nationality", "German", house),
        generate_variable_id("cigar", "Prince", house)
    ])

# Hint 14: The Norwegian lives next to the blue house
for house in range(1,NUM_HOUSES-1):
    clauses.append([
        -generate_variable_id("nationality", "Norwegian", house),
        generate_variable_id("color", "blue", house-1),
        generate_variable_id("color", "blue", house+1)
    ])
clauses.append([
        -generate_variable_id("nationality", "Norwegian", 0),
        generate_variable_id("color", "blue", 1),
    ])
clauses.append([
        -generate_variable_id("nationality", "Norwegian", 4),
        generate_variable_id("color", "blue", 3),
    ])

# Hint 15: The Norwegian lives next to the blue house
for house in range(1,NUM_HOUSES-1):
    clauses.append([
        -generate_variable_id("cigar", "Blends", house),
        generate_variable_id("drink", "water", house-1),
        generate_variable_id("drink", "water", house+1)
    ])
clauses.append([
        -generate_variable_id("cigar", "Blends", 0),
        generate_variable_id("drink", "water", 1),
    ])
clauses.append([
        -generate_variable_id("cigar", "Blends", 4),
        generate_variable_id("drink", "water", 3),
    ])


# Generate DIMACS file
filename = "einstein_riddle.cnf"
num_variables = NUM_HOUSES * sum(len(values) for values in VALUES.values())
num_clauses = len(clauses)

with open(filename, 'w') as f:
    f.write(f"p cnf {num_variables} {num_clauses}\n")
    for clause in clauses:
        f.write(" ".join(map(str, clause)) + " 0\n")

