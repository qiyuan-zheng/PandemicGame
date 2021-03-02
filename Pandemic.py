import networkx as nx
import random
import time
#nick says use pygame

def pregrame_dealing():
    global players #dict of playernames, roles, cards
    global cdeck
    
    
    
def pregame_city_deck_prep(piles):
    print("Preparing the city deck...")
    global cdeck
    random.shuffle(cdeck)
    cards = len(cdeck)
    sub1 = cdeck[:9]
    sub2 = cdeck[9:18]
    sub3 = cdeck[18:27]
    sub4 = cdeck[27:36]
    sub5 = cdeck[36:45]
    sub6 = cdeck[45:]
    subdecks = [sub1,sub2,sub3,sub4,sub5,sub6]
    index = 0
    while index<6:
        subdecks[index].append("Epidemic")
        random.shuffle(subdecks[index])
        index+=1
    cdeck = []
    while subdecks!=[]:
        subdeck = random.choice(subdecks)
        cdeck.append(subdeck)
        subdecks.remove(subdeck)
    print("The city deck is prepared!")

def pregame_infect_deck_prep():
    print("Preparing the infection deck...")
    global ideck
    global ideck_discard
    global cities
    random.shuffle(ideck)
    print("The infection deck has been prepared!")
    print()
    print("The infecting has begun!")
    i=3
    j=0
    while i>0:
        while j<3:
            city = random.choice(ideck)
            print(city,"has been infected with",i,cities[city]["color"],"cubes!")
            cities[city]["cubes"] = i
            ideck.remove(city)
            ideck_discard.append(city)
            j+=1
        j=0
        i-=1
    
network=nx.Graph()

network.add_node("Atlanta")
network.add_node("Chicago")
network.add_node("Washington")
network.add_node("New York")
network.add_node("Montreal")
network.add_node("San Francisco")
network.add_node("London")
network.add_node("Madrid")
network.add_node("Essen")
network.add_node("St. Petersburg")
network.add_node("Milan")
network.add_node("Paris")

network.add_node("Miami")
network.add_node("Mexico City")
network.add_node("Los Angeles")
network.add_node("Bogota")
network.add_node("Lima")
network.add_node("Santiago")
network.add_node("Buenos Aires")
network.add_node("Sao Paolo")
network.add_node("Kinshasa")
network.add_node("Lagos")
network.add_node("Khartoum")
network.add_node("Johannesburg")

network.add_node("Cairo")
network.add_node("Istanbul")
network.add_node("Moscow")
network.add_node("Baghdad")
network.add_node("Riyadh")
network.add_node("Karachi")
network.add_node("Chennai")
network.add_node("Mumbai")
network.add_node("Kolkatta")
network.add_node("Delhi")
network.add_node("Algiers")
network.add_node("Tehran")

network.add_node("Sydney")
network.add_node("Jakarta")
network.add_node("Manilla")
network.add_node("Ho Chi Minh City")
network.add_node("Bangkok")
network.add_node("Hong Kong")
network.add_node("Beijing")
network.add_node("Shanghai")
network.add_node("Tokyo")
network.add_node("Taipei")
network.add_node("Seoul")
network.add_node("Osaka")

#blue edges
network.add_edge("Atlanta","Chicago")
network.add_edge("Atlanta","Washington")
network.add_edge("Atlanta","Miami")
network.add_edge("Chicago","Mexico City")
network.add_edge("Chicago","Los Angeles")
network.add_edge("Chicago","San Francisco")
network.add_edge("Chicago","Montreal")
network.add_edge("Washington","New York")
network.add_edge("Washington","Miami")
network.add_edge("Washington","Montreal")
network.add_edge("New York","Montreal")
network.add_edge("New York","Madrid")
network.add_edge("London","New York")
network.add_edge("London","Madrid")
network.add_edge("London","Essen")
network.add_edge("London","Paris")
network.add_edge("Madrid","Sao Paolo")
network.add_edge("Madrid","Paris")
network.add_edge("Madrid","Algiers")
network.add_edge("San Francisco","Los Angeles")
network.add_edge("San Francisco","Tokyo")
network.add_edge("San Francisco","Manilla")
network.add_edge("Paris","Milan")
network.add_edge("Paris","Essen")
network.add_edge("Paris","Algiers")
network.add_edge("Essen","St. Petersburg")
network.add_edge("Essen","Milan")
network.add_edge("St. Petersburg","Moscow")
network.add_edge("St. Petersburg","Istanbul")

#yellow edges
network.add_edge("Miami","Mexico City")
network.add_edge("Miami","Bogota")
network.add_edge("Bogota","Lima")
network.add_edge("Bogota","Mexico City")
network.add_edge("Bogota","Sao Paolo")
network.add_edge("Bogota","Buenos Aires")
network.add_edge("Lima","Mexico City")
network.add_edge("Lima","Santiago")
network.add_edge("Buenos Aires","Sao Paolo")
network.add_edge("Lagos","Sao Paolo")
network.add_edge("Lagos","Kinshasa")
network.add_edge("Lagos","Khartoum")
network.add_edge("Khartoum","Johannesburg")
network.add_edge("Khartoum","Kinshasa")
network.add_edge("Khartoum","Cairo")
network.add_edge("Los Angeles","Sydney")
network.add_edge("Los Angeles","Mexico City")

#black edges
network.add_edge("Algiers","Istanbul")
network.add_edge("Algiers","Cairo")
network.add_edge("Istanbul","Moscow")
network.add_edge("Istanbul","Baghdad")
network.add_edge("Istanbul","Cairo")
network.add_edge("Baghdad","Tehran")
network.add_edge("Baghdad","Karachi")
network.add_edge("Baghdad","Cairo")
network.add_edge("Baghdad","Riyadh")
network.add_edge("Tehran","Moscow")
network.add_edge("Tehran","Delhi")
network.add_edge("Tehran","Karachi")
network.add_edge("Riyadh","Cairo")
network.add_edge("Karachi","Riyadh")
network.add_edge("Karachi","Mumbai")
network.add_edge("Karachi","Delhi")
network.add_edge("Mumbai","Delhi")
network.add_edge("Mumbai","Chennai")
network.add_edge("Delhi","Kolkatta")
network.add_edge("Delhi","Chennai")
network.add_edge("Kolkatta","Hong Kong")
network.add_edge("Kolkatta","Bangkok")
network.add_edge("Chennai","Kolkatta")
network.add_edge("Chennai","Jakarta")
network.add_edge("Chennai","Bangkok")

#red edges
network.add_edge("Jakarta","Sydney")
network.add_edge("Jakarta","Ho Chi Minh City")
network.add_edge("Jakarta","Bangkok")
network.add_edge("Bangkok","Ho Chi Minh City")
network.add_edge("Bangkok","Hong Kong")
network.add_edge("Hong Kong","Ho Chi Minh City")
network.add_edge("Hong Kong","Manilla")
network.add_edge("Hong Kong","Taipei")
network.add_edge("Hong Kong","Shanghai")
network.add_edge("Sydney","Manilla")
network.add_edge("Manilla","Ho Chi Minh City")
network.add_edge("Manilla","Taipei")
network.add_edge("Taipei","Osaka")
network.add_edge("Taipei","Shanghai")
network.add_edge("Shanghai","Tokyo")
network.add_edge("Shanghai","Seoul")
network.add_edge("Shanghai","Beijing")
network.add_edge("Tokyo","Osaka")
network.add_edge("Tokyo","Seoul")
network.add_edge("Seoul","Beijing")

nodes = network.nodes
events = ["Resilient Population",
          "One Quiet Night",
          "Airlift",
          "Governmany Grant",
          "Forecast"]

#assume hard mode
#piles = 6

diff = input("What difficulty would you like to play at?(Easy, Medium, Hard)")
if diff.lower()=="easy":
    epidemics = ["Epidemic!"]*4
    piles = 4
elif diff.lower()=="medium":
    epidemics = ["Epidemic!"]*5
    piles=5
elif diff.lower()=="hard":
    epidemics = ["Epidemic!"]*6
    piles=6
else:
    print("That is not an option! You lose!")
    time.sleep(3)
    exit()

cdeck = list(nodes)+events
ideck = list(nodes)
ideck_discard = []
cures = {"blue":False, "black":False, "yellow":False, "red":False}
cities = {
    "Atlanta":{"color":"blue","cubes":0,"research_station":True, "quarantined": False, "population":100},
    "Chicago":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "San Francisco":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Montreal":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "New York":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Washington":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Madrid":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "London":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Essen":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Paris":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "St. Petersburg":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Milan":{"color":"blue","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Los Angeles":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Mexico City":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Miami":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Bogota":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Lima":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Santiago":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Buenos Aires":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Sao Paolo":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Lagos":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Kinshasa":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Khartoum":{"color":"yellow","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Johannesburg":{"color":"yellow","cubes":0,"research_station":False, "quarantined":False, "population":100},
    "Cairo":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Algiers":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Istanbul":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Moscow":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Tehran":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Baghdad":{"color":"black","cubes":0,"research_station":False, "quarantined":False, "population":100},
    "Riyadh":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Delhi":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Karachi":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Mumbai":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Chennai":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Kolkatta":{"color":"black","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Sydney":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Jakarta":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Manilla":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Ho Chi Minh City":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Hong Kong":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Bangkok":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Osaka":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Shanghai":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Beijing":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Tokyo":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Taipei":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
    "Seoul":{"color":"red","cubes":0,"research_station":False, "quarantined": False, "population":100},
 }
roles = ["Dispatcher","Researcher","Medic","Scientist","Quarantine Specialist","Operations Expert","Contingency Planner"]
players={}
while True:
    try:
        temp = int(input("How many players are playing?(2-4)"))
        break
    except:
        print("Please try again.")
i=0
while i < temp:
    role = random.choice(roles)
    roles.remove(role)
    if i==0:
        name = input("What is the first player's name?")
    else:
        name = input("What is the next player's name?")
    players[name] = {"role": role}
    print(name,"is the",role+"!")
    i+=1
print()

#the dealing to the players has to go here before the decks are determined
#this will then determine the order, which is based on card population
#this means you need to edit the cities dict to add population
pregame_dealing()

#once players have initial cards, epidemic cards need to be inserted to the city deck
pregame_city_deck_prep(piles)
city_deck = []
for subdeck in cdeck: #flatten the list of lists
    for city in subdeck:
        city_deck.append(city)

#the city deck is complete and players have cards. It is now time for infection deck and infecting
pregame_infect_deck_prep()














