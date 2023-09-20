import random

first_names = ["James", "Mary", "Liam", "Olivia", "Robert", "Patricia", "Noah", "Emma", "John", "Jennifer"]
middle_names = ["Louise", "Rose", "Grace", "William", "Jane", "Elizabeth", "Thomas", "Anne", "Ann", "David"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

names = []

for first_name in first_names:
    for last_name in last_names:
        names.append(first_name + ' ' + last_name)

for first_name in first_names:
    for middle_name in middle_names:
        for last_name in last_names:
            names.append(first_name + ' ' + middle_name + ' ' + last_name)

countries = ["Switzerland", "Canada", "Sweden", "Australia", "United States", "Japan", "Germany", "New Zealand"]

vaccines = [["Pfizer", "Mainz, Germany"], ["Moderna", "Massachusetts, U.S."], ["Novavax", "Maryland, U.S."]]

with open("data_entry.tql", 'w') as f:

    for curr_vaccine in vaccines:
        query = f'insert\n\t$v isa manufacturer,\n\thas vaccine_name "{curr_vaccine[0]}",\n\thas factory_location "{curr_vaccine[1]}";\n\n'
        f.write(query)

    for name in names:
        country = random.choice(countries)
        age = str(random.randint(18, 60))
        certificate = str(random.randint(10, 99)) + chr(random.randint(65, 90)) + str(random.randint(1000, 9999)) + chr(random.randint(65, 90))
        vaccine = random.choice(vaccines)[0]
        addname = f'\ninsert\n\t$p isa person,\n\thas person_name "{name}",\n\thas country "{country}",\n\thas age {age},\n\thas certificate_no "{certificate}";\n'
        f.write(addname)
        addvac = f'\nmatch\n\t$p isa person, has person_name "{name}";\n\t$v isa manufacturer, has vaccine_name "{vaccine}";\ninsert\n\t$iv (person: $p, manufacturer: $v) isa vaccinator;\n\n'
        f.write(addvac)
