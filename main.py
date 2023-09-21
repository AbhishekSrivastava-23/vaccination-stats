from typedb.client import *

def highestVaccines():

    answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has certificate_no $no, has country $c; get $p, $no, $c; group $c; count;')

    stats = []

    for answer in answer_iterator:
        stats.append([answer._numeric._int_value, answer._owner._value])

    stats.sort(reverse = True)

    print("\nTop 3 countries with most Vaccinations:")
    for i in range(3):
        print(stats[i][1], ": ", stats[i][0])

def vaccineByAge(lower_limit, upper_limit):

    answer_iterator = read_transaction.query().match_group_aggregate(f'match $p isa person, has age >= {lower_limit}, has age <= {upper_limit}; $m isa manufacturer, has vaccine_name $v; $vcc (person: $p, manufacturer: $m) isa vaccinator; get $p, $v; group $v; count;')

    print(f"\nVaccines given to age group {lower_limit} - {upper_limit} years:")

    for answer in answer_iterator:
        print(answer._owner._value, ": ", answer._numeric._int_value)

def vaccineByCountry(country):

    country_iterator = read_transaction.query().match('match $p isa person, has country $c; get $c;')

    countries = []
    for country_pres in country_iterator:
        name = country_pres.get("c")
        countries.append(name.get_value())

    if country not in countries:
        print("No entries for the given country!")
        return

    answer_iterator = read_transaction.query().match_group_aggregate(f'match $p isa person, has country = "{country}"; $m isa manufacturer, has vaccine_name $v; $vcc (person: $p, manufacturer: $m) isa vaccinator; get $p, $v; group $v; count;')

    print(f"\nVaccines provided in {country}:")
    for answer in answer_iterator:
        print(answer._owner._value, ": ", answer._numeric._int_value)

def avgAgeByCountry():

    answer_iterator = read_transaction.query().match_group_aggregate('match $p isa person, has country $c, has age $a; get $c, $a; group $c; mean $a;')

    print("\nAverage age of people vaccinated in each country:\n")

    for answer in answer_iterator:
        print(answer._owner._value, ": ", round(answer._numeric._float_value), "years")

port = input("Enter port (For using default port, 1729, press Enter): ")
if port == '':
    port = "localhost:1729"

database_name = input("Enter name of the DataBase: ")
    
with TypeDB.core_client(port) as client:
    with client.session(database_name, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as read_transaction:

            while (True):

                print("\nMENU")
                print("1. Display top 3 countries with most vaccinations")
                print("2. Display vaccine-wise stats for a given age group")
                print("3. Display vaccine-wise stats for a given country")
                print("4. Display average age of people vaccinated in each country")
                print("5. Exit")
                choice = input("Enter your choice: ")

                match choice:

                    case '1':
                        highestVaccines()

                    case '2':
                        try:
                            lower_lim = int(input("\nEnter lower limit: "))
                            upper_lim = int(input("Enter upper limit: "))
                            if (lower_lim > upper_lim):
                                print("Invalid Input")
                                continue
                            vaccineByAge(lower_lim, upper_lim)
                        except:
                            print("Invalid Input")

                    case '3':
                        country = input("\nEnter country name: ")
                        vaccineByCountry(country)

                    case '4':
                        avgAgeByCountry()

                    case '5':
                        print("\nTHANK YOU!\n")
                        break

                    case _:
                        print("\nInvalid choice")
