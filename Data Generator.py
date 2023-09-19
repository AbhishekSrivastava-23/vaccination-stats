import random

first_names = ["James", "Mary", "Liam", "Olivia", "Robert", "Patricia", "Noah", "Emma", "John", "Jennifer"]
middle_names = ["Louise", "Rose", "Grace", "William", "Jane", "Elizabeth", "Thomas", "Anne", "Ann", "David"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

names = []

for i in range(10):
    for j in range(10):
        names.append(first_names[i] + ' ' + last_names[i])

for i in range(10):
    for j in range(10):
        for k in range(10):
            names.append(first_names[i] + ' ' + middle_names[j] + ' ' + last_names[k])

countries = ["Switzerland", "Canada", "Sweden", "Australia", "United States", "Japan", "Germany", "New Zealand"]

vaccines = [["Pfizer", "Mainz, Germany"], ["Moderna", "Massachusetts, U.S."], ["Novavax", "Maryland, U.S."]]

random.shuffle(names)

with open("E:/Vaccination DataBase/data_entry.tql", 'w') as f:

    for i in range(3):
        query = 'insert\n\t$v isa manufacturer,\n\thas vaccine_name "' + vaccines[i][0] + '",\n\thas factory_location "' + vaccines[i][1] + '";\n\n'
        f.write(query)

    for name in names:
        country = countries[random.randint(0, 7)]
        age = str(random.randint(18, 60))
        certificate = str(random.randint(10, 99)) + chr(random.randint(65, 90)) + str(random.randint(1000, 9999)) + chr(random.randint(65, 90))
        vaccine = vaccines[random.randint(0, 2)][0]
        addname = '\ninsert\n\t$p isa person,\n\thas person_name "' + name + '",\n\thas country "' + country + '",\n\thas age ' + age + ',\n\thas certificate_no "' + certificate + '";\n'
        f.write(addname)
        addvac = '\nmatch\n\t$p isa person, has person_name "' + name + '";\n\t$v isa manufacturer, has vaccine_name "' + vaccine + '";\ninsert\n\t$iv (person: $p, manufacturer: $v) isa vaccinator;\n\n'
        f.write(addvac)