import networkx as nx
import random
import time
#nick says use pygame

def pregame_dealing():
    global players #dict of playernames, roles, cards
    global cdeck
    global cdeck_discard
    random.shuffle(cdeck)
    if len(players)==4:
        for player in players:
            card1 = cdeck.pop()
            card2 = cdeck.pop()
            players[player]["cards"] = [card1,card2]
            cdeck_discard.append(card1)
            cdeck_discard.append(card2)
            print(players[player]["name"]+str("'s")+" cards are:", players[player]["cards"])
    elif len(players)==3:
        for player in players:
            card1 = cdeck.pop()
            card2 = cdeck.pop()
            card3 = cdeck.pop()
            players[player]["cards"] = [card1,card2,card3]
            cdeck_discard.append(card1)
            cdeck_discard.append(card2)
            cdeck_discard.append(card3)
            print(players[player]["name"]+str("'s")+" cards are:", players[player]["cards"])
    else:
        for player in players:
            card1 = cdeck.pop()
            card2 = cdeck.pop()
            card3 = cdeck.pop()
            card4 = cdeck.pop()
            players[player]["cards"] = [card1,card2,card3,card4]
            cdeck_discard.append(card1)
            cdeck_discard.append(card2)
            cdeck_discard.append(card3)
            cdeck_discard.append(card4)
            print(players[player]["name"]+str("'s")+" cards are:", players[player]["cards"])
        
    
def pregame_city_deck_prep(piles):
    print("Preparing the city deck...")
    global cdeck
    random.shuffle(cdeck)
    sublist_lengths = []
    if len(players)==4 or len(players)==2:
        if piles==4:
            sublist_lengths = [11,11,11,12]
        elif piles==5:
            sublist_lengths = [9,9,9,9,9]            
        else:
            sublist_lengths = [8,8,8,7,7,7]
    else: #there must be 3 players
        if piles==4:
            sublist_lengths = [10,10,11,11]            
        elif piles==5:
            sublist_lengths = [8,8,8,9,9]
        else:
            sublist_lengths = [7,7,7,7,7,7]
    subdecks = []
    i=0
    start=0
    while i<piles:
        subdeck = cdeck[start:start+sublist_lengths[i]]
        subdecks.append(subdeck)
        start = start + len(subdeck)
        i+=1
    print()
    index = 0
    while index<piles:
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
    global infect_deck_discard
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
            infect_deck_discard.append(city)
            j+=1
        j=0
        i-=1

def turn_checker():
    global turn
    global players
    print("It is",players[turn]["name"]+str("'s"),"turn as the",players[turn]["role"]+str("!"))
    

def menu():
    print("Enter the number of your first action or 'd' to display the board:")
    print("1 Walk")
    print("2 Fly")
    print("3 Exchange Information (Trade Cards)")
    print("4 Pickup Cube(s)")
    print("5 Cure a Disease")
    print("6 Build a Research Station")
    print("7 Travel to another research Station")
    print("8 Spend an Event Card")
    print("d Display Board")
    x=input()
    return x

def is_valid_action(action):
    try:
        action = int(action)
        if action>=1 and action<=8:
            return True
        else:
            return False
    except:
        return action=="d"

def resolve_action(action):
    if action=="1":
        return walk()
    elif action=="2":
        return direct_flight()
    elif action=="3":
        return exchange_info()
    elif action=="4":
        return pickup()
    elif action=="5":
        return cure()
    elif action=="6":
        return research()
    elif action=="7":
        return goto_research_station()
    elif action=="8":
        return eventcard()
    return display_board()

def walk():
    global players
    current = players[turn]['location']
    connections = list(network.neighbors(current))
    i=1
    print("Where would you like to walk to?")
    for connection in connections:
        print(i,connection)
        i+=1
    choice = input()
    try:
        choice = int(choice)
        if choice>=1 and choice < i:
            players[turn]['location'] = connections[choice-1]
        else:
            print("else")
            print("Not a valid move")
            return False
    except ValueError:
        print("except")
        print("Not a valid move")
        return False
    return True

def direct_flight():
    global players
    global cdeck_discard
    cards = players[turn]['cards']
    print()
    print("Enter the number of the city you would like to go to:")
    i=1
    for card in cards:
        print(i,card)
        i+=1
    choice = input()
    try:
        choice = int(choice)
        if choice>=1 and choice<=len(cards):
            card = players[turn]['cards'][choice-1]
            if card not in events:
                players[turn]['location'] = card
                players[turn]['cards'].remove(card)
                cdeck_discard.append(card)
                return True
            else:
                print("You cannot take a direct flight to an event card")
                return False
        else:
            print("Sorry that action is invalid")
            return False
    except ValueError:
        print("Please enter a valid number next time")
        return False

def exchange_info():
    print("I am exchanging info!")
    return True

def pickup():
    print("I am picking up cubes!")
    return True

def cure():
    print("I am curing!")
    return True

def research():
    global cities
    global cdeck_discard
    global players
    cards = players[turn]['cards']
    if players[turn]['location'] in cards:
        card = players[turn]['location']
        cities[card]['research_station'] = True
        cdeck_discard.append(card)#spend it to make reserach station
        players[turn]['cards'].remove(card)
        return True
    else:
        print("You do not have that card!")
        return False

def goto_research_station():
    global players
    city = players[turn]['location']
    if cities[city]['research_station']==True:
        i=0
        stations = []
        for othercity in cities:
            if cities[othercity]['research_station']==True and othercity!=city:
                stations.append(othercity)
                print(i+1,othercity)
                i+=1
        choice = input()
        try:
            choice = int(choice)
            if choice>=1 and choice<=len(stations):
                players[turn]['location'] = stations[i-1]
                return True
            else:
                print("Not a valid number")
                return False
        except ValueError:
            return False
    else:
        print("that action is not valid")
        return False
                
                
        
    return True

def eventcard():
    return True

def display_board():
    print("The board is being displayed! jk")
    return False

def draw_two():
    global city_deck
    global players
    global turn
    global cdeck_discard

    card1 = city_deck.pop()
    card2 = city_deck.pop()
    print(players[turn]["name"],"drew",card1+"!")
    print(players[turn]["name"],"drew",card2+"!")
    
    if card1!="Epidemic":
        players[turn]["cards"].append(card1)
    else:
        cdeck_discard.append(card1)
    if card2!="Epidemic":
        players[turn]["cards"].append(card2)
    else:
        cdeck_discard.append(card2)
    #resolve epidemics
    if card1=="Epidemic" and card2=="Epidemic":
        #resolve_double_epidemic()
        print("OH NO DOUBLE EPIDEMIC DDD:<")
    elif card1=="Epidemic" or card2=="Epidemic":
        resolve_epidemic()
        print("OH NO EPIDEMIC DDD:<")
    #more than 7 cards?
    resolve_hand_limit()

def resolve_epidemic():
    #3 things that happen during an epidemic: reshuffle the infection discard pile
    global card_counter_index
    global infect_deck
    global infect_deck_discard
    global cities
    card_counter_index+=1 #increase the counter
    infected = infect_deck[-1] 
    infect_deck = infect_deck[:-1]
    infect_deck_discard.append(infected)
    print(infected,"has been infected with 3 cubes!")
    place_cubes(infected,3, cities[infected]['color']) #put 3 cubes on last card
    reshuffle()
    infect()
    

def resolve_double_epidemic():
    print("This test probably won't happen for a while")
    pass

def resolve_hand_limit():
    global players
    global turn
    global cdeck_discard
    while len(players[turn]["cards"])>7:
        while True:
            print("You have more than 7 cards!")
            print("Please type the number of the card that you would like to remove")
            i=0
            for card in players[turn]["cards"]:
                print(str(i+1), players[turn]['cards'][i])
                i+=1
            discard = input()
            try:
                discard = int(discard)
                if discard>=1 and discard<=len(players[turn]['cards']):
                    #remove from hand
                    #players[turn]['cards'] = players[turn]['cards'][:discard] + players[turn]['cards'][discard+1:]
                    removed = players[turn]['cards'][discard-1]
                    players[turn]['cards'].remove(removed)
                    #add to discard pile
                    cdeck_discard.append(removed)
                    break
                else:
                    print("Please enter a valid number")
            except:
                print("Please enter a valid number")

"""
   0       1    2     3        4         5         6       7   
['miami','LA','dc','home','ur place','sewer','hospital','mcd's']
which card do you want to get rid of?(1-8)
8
currently: 



"""
        
def infect():
    global infect_deck
    global infect_deck_discard
    global cities
    i=0
    while i<card_counter[card_counter_index]:
        infected = infect_deck.pop()
        print(infected,"has been infected with 1",cities[infected]['color'],"cube!")
        time.sleep(1)
        place_cubes(infected,1,cities[infected]['color'])
        infect_deck_discard.append(infected)
        i+=1
    
#this function takes a city and number of cubes to be placed and updates the cities dict
def place_cubes(city, cubes, color, outbreakchain = []):
    global cities
    global outbreaks
    if cities[city]['cubes'][color] + cubes > 3 and cities[city]["quarantined"]==False and city not in outbreakchain:
        print("Outbreak!")
        time.sleep(1)
        outbreaks+=1
        cities[city]['cubes'][color] = 3
        resolve_outbreak(city,outbreakchain+[city], color)
    elif city in outbreakchain:
        pass #break the chain
    else:
        #print(city,"has been infected with",cubes,"cubes")
        cities[city]['cubes'][color] += cubes #place the cubes
        
#this function will take a city and place one cube on each unprotected neighboring city
#need to make sure the outbreaks do not loop into each other - will do this with citylist
def resolve_outbreak(city, outbreakchain, color):
    global network
    connections = nx.neighbors(network,city)
    print("The connections to this city are:", connections)
    for connection in connections:
        place_cubes(connection,1,color,outbreakchain)
        

#this function shuffles the infection discard pile and places it back atop the infection deck
def reshuffle():
    global infect_deck_discard
    global infect_deck
    random.shuffle(infect_deck_discard)
    infect_deck = infect_deck_discard + infect_deck
    infect_deck_discard = []

#the making of the graph to determine connections 
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
#edges
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
          "Government Grant",
          "Forecast"]
cdeck = list(nodes)+events
ideck = list(nodes)
infect_deck_discard = []
cdeck_discard = []
outbreaks = 0
card_counter_index = 0
card_counter = [2,2,2,3,3,4,4]
research_stations = 5 #1 is starting in Atlanta by default
diseases = {"blue":{"cured":False,"eradicated":False,"cubes":24}, "black":{"cured":False,"eradicated":False,"cubes":24},
         "yellow":{"cured":False,"eradicated":False,"cubes":24}, "red":{"cured":False,"eradicated":False,"cubes":24}}
cities = {
    "Atlanta":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":True, "quarantined": False, "population":100},
    "Chicago":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "San Francisco":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Montreal":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "New York":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Washington":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Madrid":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "London":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Essen":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Paris":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "St. Petersburg":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Milan":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Los Angeles":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Mexico City":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Miami":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Bogota":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Lima":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Santiago":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Buenos Aires":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Sao Paolo":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Lagos":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Kinshasa":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Khartoum":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Johannesburg":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined":False, "population":100},
    "Cairo":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Algiers":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Istanbul":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Moscow":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Tehran":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Baghdad":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined":False, "population":100},
    "Riyadh":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Delhi":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Karachi":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Mumbai":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Chennai":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Kolkatta":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Sydney":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Jakarta":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Manilla":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Ho Chi Minh City":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Hong Kong":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Bangkok":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Osaka":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Shanghai":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Beijing":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Tokyo":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Taipei":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
    "Seoul":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":100},
 }
roles = ["Dispatcher","Researcher","Medic","Scientist","Quarantine Specialist","Operations Expert","Contingency Planner"]
players={}




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


while True:
    try:
        temp = int(input("How many players are playing?(2-4)"))
        if temp>=2 and temp<=4:
            break
        else:
            print("Please enter a valid number of players.")
            pass #keep going 
    except:
        print("Please try again.")
i=1
while i <=temp:
    role = random.choice(roles)
    roles.remove(role)
    if i==1:
        print("What is the first player's name?")
        time.sleep(.5)
        name = input()
    else:
        print("What is the next player's name?")
        time.sleep(.5)
        name = input()
    players[i] = {"name":name, "role": role, "location":"Atlanta"}
    print(name,"is the",role+"!")
    time.sleep(1)
    i+=1
print()

#the dealing to the players has to go here before the decks are determined
#this will then determine the order, which is based on card population
#this means you need to edit the cities dict to add population
pregame_dealing()
time.sleep(2)

#once players have initial cards, epidemic cards need to be inserted to the city deck
pregame_city_deck_prep(piles)
city_deck = []
for subdeck in cdeck: #flatten the list of lists
    for city in subdeck:
        city_deck.append(city)

#the city deck is complete and players have cards. It is now time for infection deck and infecting
pregame_infect_deck_prep()
infect_deck = ideck[:] #rename the vars to be consistent
time.sleep(2)

print()
print("You are ready to play!")
print()
time.sleep(2)
#main game loop - create a menu of actions and take input for that.
#               - create methods for each of those actions
#               - dtermine the order before all of this happens
turn = 1
#while you have not yet lost
while outbreaks<8 and len(cdeck)>0: #check for cubes during infection steps
    actions = 4
    turn_checker()
    time.sleep(1)
    #do 4 actions
    while actions>0:
        print("You have",actions,"actions remaining.")
        #this loop is to ensure a proper action
        while True:
            action = menu()
            if is_valid_action(action): #make sure they put in a valid action choice
                if resolve_action(action): #if the action is possible
                    actions-=1 #count it as an action
                    break
                else:
                    print("That action is not possible. Please try again.")
            else:
                print("Please enter a valid action")
                pass
    #draw two city cards
    draw_two() #calls resolve_epidemic() and resolve_hand_limit()
    #infect cities
    infect()
    #whose turn?
    if turn==len(players):
        turn = 1 #start the rotation over
    else:
        turn+=1 #else next person
        
    











