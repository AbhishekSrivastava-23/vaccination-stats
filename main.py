from typedb.client import *

def highestVaccines(session):

    with session.transaction(TransactionType.READ) as read_transaction:

        answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has certificate_no $no, has country $c; get $p, $no, $c; group $c; count;')

        stats = []

        for answer in answer_iterator:
            stats.append([answer._numeric._int_value, answer._owner._value])

        stats.sort(reverse = True)

        if len(stats) == 0:
            print("\nNo entries present in the Database!")
            return

        if len(stats) < 3:
            print("\nEntries for only", len(stats), "countries present!")
            print("Top", len(stats), "countries with most Vaccinations:")
            for country_stat in stats:
                print(country_stat[1], ":", country_stat[0])
            return

        print("\nTop 3 countries with most Vaccinations:")
        for i in range(3):
            print(stats[i][1], ":", stats[i][0])

def vaccineByAge(lower_limit, upper_limit, session):

    with session.transaction(TransactionType.READ) as read_transaction:

        answer_iterator = read_transaction.query().match_group_aggregate(f'match $p isa person, has age >= {lower_limit}, has age <= {upper_limit}; $m isa manufacturer, has vaccine_name $v; $vcc (person: $p, manufacturer: $m) isa vaccinator; get $p, $v; group $v; count;')

        if all(False for _ in answer_iterator):
            print("No entries for the given age group!")
            return

        print(f"\nVaccines given to age group {lower_limit} - {upper_limit} years:")

        for answer in answer_iterator:
            print(answer._owner._value, ":", answer._numeric._int_value)

def vaccineByCountry(country, session):

    with session.transaction(TransactionType.READ) as read_transaction:

        answer_iterator = read_transaction.query().match_group_aggregate(f'match $p isa person, has country = "{country}"; $m isa manufacturer, has vaccine_name $v; $vcc (person: $p, manufacturer: $m) isa vaccinator; get $p, $v; group $v; count;')

        if all(False for _ in answer_iterator):
            print("No entries for the given country!")
            return

        print(f"\nVaccines provided in {country}:")
        for answer in answer_iterator:
            print(answer._owner._value, ":", answer._numeric._int_value)

def avgAgeByCountry(session):

    with session.transaction(TransactionType.READ) as read_transaction:

        answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has country $c, has age $a; get $c, $a; group $c; mean $a;')

        print("\nAverage age of people vaccinated in each country:\n")

        for answer in answer_iterator:
            print(answer._owner._value, ":", round(answer._numeric._float_value), "years")

port = input("Enter address and port (For using default 'localhost:1729', press Enter): ")
if port == '':
    port = "localhost:1729"

database_name = input("Enter the name of the Database: ")
    
while (True):

    print("\nMENU")
    print("1. Display top 3 countries with most vaccinations")
    print("2. Display vaccine-wise stats for a given age group")
    print("3. Display vaccine-wise stats for a given country")
    print("4. Display average age of people vaccinated in each country")
    print("5. Exit")
    choice = input("Enter your choice: ")

    with TypeDB.core_client(port).session(database_name, SessionType.DATA) as session:

        match choice:

            case '1':
                highestVaccines(session)

            case '2':
                try:
                    lower_lim = int(input("\nEnter lower limit: "))
                    upper_lim = int(input("Enter upper limit: "))
                    if (lower_lim > upper_lim):
                        print("Invalid Input")
                        continue
                    vaccineByAge(lower_lim, upper_lim, session)
                except:
                    print("Invalid Input")

            case '3':
                country = input("\nEnter country name: ")
                vaccineByCountry(country, session)

            case '4':
                avgAgeByCountry(session)

            case '5':
                print("\nTHANK YOU!\n")
                break

            case _:
                print("\nInvalid choice")
