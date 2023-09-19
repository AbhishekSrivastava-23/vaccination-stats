from typedb.client import *

def highestVaccines():

    with TypeDB.core_client("localhost:1729") as client:
        with client.session("vaccination_schema", SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:

                answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has country $c; get $p, $c; group $c; count;')

                stats = []

                for answer in answer_iterator:
                    stats.append([answer._numeric._int_value, answer._owner._value])

                stats.sort(reverse = True)

                print("\nTop 3 countries with most Vaccinations:")
                for i in range(3):
                    print(stats[i][1], " : ", stats[i][0])

def vaccineByAge(l, r):
    
    with TypeDB.core_client("localhost:1729") as client:
        with client.session("vaccination_schema", SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:

                answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has age >= ' + str(l) + ', has age <= ' + str(r) + '; $m isa manufacturer, has vaccine_name $v; $vcc (person: $p, manufacturer: $m) isa vaccinator; get $p, $v; group $v; count;')

                print("\nVaccines given to age group", l, '-', r, "years:")

                for answer in answer_iterator:
                    print(answer._owner._value, " : ", answer._numeric._int_value)

def vaccineByCountry(country):

    with TypeDB.core_client("localhost:1729") as client:
        with client.session("vaccination_schema", SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:

                country_iterator = read_transaction.query().match('match $p isa person, has country $c; get $c;')

                countries = []
                for country_pres in country_iterator:
                    name = country_pres.get("c")
                    countries.append(name.get_value())

                if country not in countries:
                    print("Country not found")
                    return

                answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has country = "' + country + '"; $m isa manufacturer, has vaccine_name $v; $vcc (person: $p, manufacturer: $m) isa vaccinator; get $p, $v; group $v; count;')

                print("\nVaccines provided in", country, ":")
                for answer in answer_iterator:
                    print(answer._owner._value, " : ", answer._numeric._int_value)

def avgAgeByCountry():

    with TypeDB.core_client("localhost:1729") as client:
        with client.session("vaccination_schema", SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:

                answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has country $c, has age $a; get $c, $a; group $c; mean $a;')

                print("\nAverage age of people vaccinated in each country:\n")

                for answer in answer_iterator:
                    print(answer._owner._value, " : ", round(answer._numeric._float_value, 1), "years")
    

while (True):

    print("\nMENU")
    print("1. Display countries with most vaccinations")
    print("2. Display vaccine-wise stats for a given age group")
    print("3. Display vaccine-wise stats for a given country")
    print("4. Display average age of people vaccinated in each country")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if (choice == '1'):
        highestVaccines()

    elif (choice == '2'):
        l = int(input("\nEnter lower limit: "))
        r = int(input("Enter upper limit: "))
        if (l > r):
            print("Invalid Input")
            continue
        vaccineByAge(l, r)

    elif (choice == '3'):
        country = input("\nEnter country name: ")
        vaccineByCountry(country)

    elif (choice == '4'):
        avgAgeByCountry()

    elif (choice == '5'):
        print("\nTHANK YOU!\n")
        break

    else:
        print("\nInvalid choice")