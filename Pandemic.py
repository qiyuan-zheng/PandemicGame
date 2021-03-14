import networkx as nx
import random
import time
import matplotlib as plt
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
            place_cubes(city,i,cities[city]['color'])
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
    if actions==4:
        print("Enter the option for your first action:")
    else:
        print("Enter the option for your next action:")
    print("1 Walk")
    print("2 Fly")
    print("3 Exchange Information (Trade Cards)")
    print("4 Pickup Cube(s)")
    print("5 Cure a Disease")
    print("6 Build a Research Station")
    print("7 Travel to another research Station")
    print("8 Spend an Event Card")
    print("c Display Cards")
    print("f Display Cubes")
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
        return action=="d" or action=="c" or action=="f"

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
    elif action=="c":
        return display_cards()
    elif action=="f":
        return display_cubes()
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
    global players
    city = players[turn]['location']
    cards = players[turn]['cards']
    samespace = []
    for player in players:
        if players[player]['location']==city and player!=turn:
            samespace.append(str(player))
    print('samespace', samespace)
    print("Are you(G) giving a card or (T)taking a card?")
    x = input()
    if x=="G":
        if players[turn]['role']=="Researcher" or city in cards:
            print("Which player are you giving the card to?")
            for player in samespace:
                print(player,players[int(player)]['name'],'the',players[int(player)]['role'])
            choice3 = input() 
            if choice3 in samespace:
                if players[turn]['role']=="Researcher":
                    m = 1
                    print("What card would you like to give?")
                    for card in cards:
                        print(m,card)
                        m+=1
                    try:
                        card = int(input())
                        if card>=1 and card<=len(cards):
                            #give that card
                            players[int(choice3)]['cards'].append(players[turn]['cards'][card-1])
                            players[turn]['cards'].remove(players[turn]['cards'][card-1])
                            print("Exchange Successful!")
                            return True
                    except ValueError:
                        return False
                else:
                    #trade the card of the city you are in
                    players[int(choice3)]['cards'].append(city)
                    players[turn]['cards'].remove(city)
                    print("Exchange successful!")
                    return True
            else:
                return False
    elif x=="T":
        print("Choose the player you would like to take a card from")
        for player in samespace:
            print(player,players[int(player)]['name'],'the',players[int(player)]['role'])
        choice = input() #which player

        if choice in samespace:
            if players[int(choice)]['role']=="Researcher": #people can take any card from researcher
                j=1
                print("Which card would you like to take?")
                for card in players[int(choice)]['cards']:
                    print(j,card)
                    j+=1
                choice2 = input()
                try:
                    choice2=int(choice2)
                    if choice2>=1 and choice2<=len(players[int(choice)]['cards']):
                        #trade that card
                        players[turn]['cards'].append(players[int(choice)]['cards'][choice2-1])
                        players[int(choice)]['cards'].remove(players[int(choice)]['cards'][choice2-1])
                        print("Exchange successful!")
                        return True
                    else:
                        return False
                except:
                    return False
                    
                return True
            #elif normal player
            elif city in players[int(choice)]['cards']: #people may only take same-city cards from non-researchers
                #trade that card
                players[turn]['cards'].append(city)
                players[int(choice)]['cards'].remove(city)
                print("Exchange successful!")
                return True
            else:
                return False
        else:
            return False
        
    else:
        return False       

#this function returns a list of the color of cubes in the current city
def get_cube_types():
    cube_types = []
    city = players[turn]['location']
    for color in cities[city]['cubes']:
        if cities[city]['cubes'][color]>0:
            cube_types.append(color)
    return cube_types

def pickup():
    global cities
    global diseases
    cube_types = get_cube_types() 
    if len(cube_types)==0:
        print("No cubes here!")
        return False
    elif len(cube_types)==1:
        color = cube_types[0]
    else:
        i=0
        print("What color cube do you want to pick up?")
        for color in cube_types:
            print(i+1, color)
        choice = input()
        try:
            choice = int(choice)
            if choice>=1 and choice<=len(cube_types):
                color = cube_types[choice-1]
            else:
                return False
        except:
            return False    
    if players[turn]['role']=="Medic" and diseases[color]['cured']==False:
        diseases[color]['cubes']+= cities[players[turn]['location']]['cubes'][color]
        cities[players[turn]['location']]['cubes'][color] = 0
        print("The medic cleared",players[turn]['location']+"!")
    elif players[turn]['role']=="Medic" and diseases[color]['cured']:
        print("This will happen by default from the medic visiting here. Not counting as an action")
        return False
    elif diseases[color]['cured']:
        diseases[color]['cubes']+= cities[players[turn]['location']]['cubes'][color]
        cities[players[turn]['location']]['cubes'][color] = 0
        print(players[turn]['role'],"cleared",players[turn]['location']+"!")

    else:
        diseases[color]['cubes']+= 1
        cities[players[turn]['location']]['cubes'][color] -= 1
        print(players[turn]['role'],"cleared 1 cube off of",players[turn]['location']+"!")
    return True

def cure():
    city = players[turn]['location']
    if cities[city]['research_station']:
        print("Which disease would you like to cure?")
        for disease in diseases:
            print(disease)
        choice = input()
        if choice not in diseases:
            return False
        count=0
        turn_in=[]
        for card in players[turn]['cards']:
            if card not in events and cities[card]['color']==choice:
                turn_in.append(card)
        count=len(turn_in)
        if (players[turn]['role']=="Scientist" and count==4) or count==5:    
            cure_helper(turn_in,choice)
            return True
        elif (players[turn]['role']=="Scientist" and count>4) or count>5:
            turn_in = which_cards(turn_in)
            cure_helper(turn_in,choice)
            return True
        return False
    return False

def which_cards(turn_in):
    if players[turn]['role']=="Scientist":
        limit=4
    else:
        limit=5
    while len(turn_in)>limit:
        print("Enter a card would you like to keep(not turn in)")
        for card in turn_in:
            print(card)
        keep = input()
        if keep not in turn_in:
            print("I think this would turn them all in...")
            break
        else:
            turn_in.remove(card)
    return turn_in
            
    
def cure_helper(turn_in, disease):
    global players
    global diseases
    global cdeck_discard
    print('turn_in',turn_in)
    print('cards',players[turn]['cards'])
    for card in turn_in:
        players[turn]['cards'].remove(card)
        cdeck_discard.append(card)
    diseases[disease]['cured']=True
        
def research():
    global cities
    global cdeck_discard
    global players
    global research_stations
    city = players[turn]['location']
    if players[turn]['role']=="Operations Expert" and research_stations>0 and cities[city]['research_station']==False:
        cities[city]['research_station'] = True
        research_stations-=1
        return True
    else:
        cards = players[turn]['cards']
        if players[turn]['location'] in cards and research_stations>0:
            card = players[turn]['location']
            cities[card]['research_station'] = True
            cdeck_discard.append(card)#spend it to make reserach station
            players[turn]['cards'].remove(card)
            research_stations-=1
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
        print("That action is not valid")
        return False
    return True

def eventcard():
    return True

def display_cards():
    for player in players:
        print(players[player]['name']+"'s cards:", players[player]['cards'])
    return False #not an action

def display_cubes():
    for city in cities:
        if cities[city]['cubes']['red']==0 and cities[city]['cubes']['blue']==0  and cities[city]['cubes']['yellow']==0  and cities[city]['cubes']['black']==0:
            pass
        else:
            colors = ['red','black','blue','yellow']
            acc = city+" has: "
            for color in colors:
                if cities[city]['cubes'][color]>0:
                    acc+= str(cities[city]['cubes'][color])+color+" cubes and "
            print(acc)
                    
def display_board():
    print("I am displaying the board")
    return False #not an action

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
        print("OH NO EPIDEMIC DDD:<")
        resolve_epidemic()
        
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
    #infect() #get rid of this line!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #why is the infect discard not going back on top?

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

def infect():
    global infect_deck
    global infect_deck_discard
    global cities
    i=0
    while i<card_counter[card_counter_index]:
        infected = infect_deck.pop(0)
        print(infected,"has been infected with 1",cities[infected]['color'],"cube!")
        time.sleep(1)
        place_cubes(infected,1,cities[infected]['color'])
        infect_deck_discard.append(infected)
        i+=1
    
#this function takes a city and number of cubes to be placed and updates the cities dict
def place_cubes(city, cubes, color, outbreakchain = []):
    global cities
    global outbreaks
    global diseases
    if cities[city]['cubes'][color] + cubes > 3 and cities[city]["quarantined"]==False and city not in outbreakchain:
        print("Outbreak!")
        diseases[color]['cubes']-= 3 - cities[city]['cubes'][color] #subtract the amount of cubes to get to 3
        time.sleep(1)
        outbreaks+=1
        cities[city]['cubes'][color] = 3
        resolve_outbreak(city,outbreakchain+[city], color)
    elif city in outbreakchain:
        pass #break the chain
    else:
        diseases[color]['cubes'] -= cubes
        cities[city]['cubes'][color] += cubes #place the cubes
        
#this function will take a city and place one cube on each unprotected neighboring city
#need to make sure the outbreaks do not loop into each other - will do this with citylist
def resolve_outbreak(city, outbreakchain, color):
    connections = nx.neighbors(network,city)
    acc=[]
    for connection in connections:
        acc.append(connection)
    print("The connections to this city are:", acc)
    for connection in connections:
        place_cubes(connection,1,color,outbreakchain)
        

#this function shuffles the infection discard pile and places it back atop the infection deck
def reshuffle():
    global infect_deck_discard
    global infect_deck
    random.shuffle(infect_deck_discard)
    infect_deck = infect_deck_discard + infect_deck
    infect_deck_discard = []

#this is a function that is called at the end of every medic action to ensure he clears infected cities he passes through
def medic_passive(city):
    global cities
    global diseases
    for disease in diseases:
        if diseases[disease]['cured']==True:
            diseases[disease]['cubes']+= cities[city]['cubes'][diseases[disease]['name']] 
            cities[city]['cubes'][diseases[disease]['name']] = 0
            print("The medic cleared",city,"upon passing through!")
    
#this will determine the player with the lowest population. they will start the game            
def who_is_first():
    least = 1000000000
    least_player=0
    for player in players:
        for card in players[player]['cards']:
            if card not in events and cities[card]['population']<least:
                least = cities[card]['population']
                least_player = player
    return least_player
    
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
network.add_edge("Kinshasa","Johannesburg")
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
diseases = {"blue":{"name":"blue","cured":False,"eradicated":False,"cubes":24}, "black":{"name":"black","cured":False,"eradicated":False,"cubes":24},
         "yellow":{"name":"yellow","cured":False,"eradicated":False,"cubes":24}, "red":{"name":"red","cured":False,"eradicated":False,"cubes":24}}
cities = {
    "Atlanta":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":True, "quarantined": False, "population":4715000},
    "Chicago":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":9121000},
    "San Francisco":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":5864000},
    "Montreal":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":3429000},
    "New York":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":20464000},
    "Washington":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":4679000},
    "Madrid":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":5427000},
    "London":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":8586000},
    "Essen":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":575000},
    "Paris":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":10755000},
    "St. Petersburg":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":4879000},
    "Milan":{"color":"blue","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":5232000},
    "Los Angeles":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":14900000},
    "Mexico City":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":19463000},
    "Miami":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":5582000},
    "Bogota":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":8702000},
    "Lima":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":9121000},
    "Santiago":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":6015000},
    "Buenos Aires":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":13639000},
    "Sao Paolo":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":20186000},
    "Lagos":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":11547000},
    "Kinshasa":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":9046000},
    "Khartoum":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":4887000},
    "Johannesburg":{"color":"yellow","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined":False, "population":3888000},
    "Cairo":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":17718000},
    "Algiers":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":2946000},
    "Istanbul":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":13576000},
    "Moscow":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":15512000},
    "Tehran":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":7419000},
    "Baghdad":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined":False, "population":6204000},
    "Riyadh":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":5037000},
    "Delhi":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":22242000},
    "Karachi":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":20711000},
    "Mumbai":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":16910000},
    "Chennai":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":8865000},
    "Kolkatta":{"color":"black","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":14374000},
    "Sydney":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":3785000},
    "Jakarta":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":26063000},
    "Manilla":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":20767000},
    "Ho Chi Minh City":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":8314000},
    "Hong Kong":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":7106000},
    "Bangkok":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":7151000},
    "Osaka":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":2871000},
    "Shanghai":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":13482000},
    "Beijing":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":17311000},
    "Tokyo":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":13189000},
    "Taipei":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":8338000},
    "Seoul":{"color":"red","cubes":{"blue":0,"black":0,"yellow":0,"red":0},"research_station":False, "quarantined": False, "population":22547000},
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

#
#main game loop
#

turn = who_is_first()
#while you have not yet lost
while outbreaks<8 and len(cdeck)>=0 and diseases['black']['cubes']>0 and diseases['blue']['cubes']>0 and diseases['red']['cubes']>0 and diseases['yellow']['cubes']>0:
    actions = 4
    turn_checker()
    time.sleep(1)
    #do 4 actions
    while actions>0:
        print(players[turn]['name'],'the',players[turn]['role'],'has',actions,"actions remaining.")
        #this loop is to ensure a proper action
        while True:
            action = menu()
            if is_valid_action(action): #make sure they put in a valid action choice
                if resolve_action(action): #if the action is possible
                    actions-=1 #count it as an action
                    #additional medic check
                    if players[turn]['role']=='Medic': #the medic clears cities of cured diseases everywhere he steps so check for that as he goes
                        medic_passive(players[turn]['location'])
                    break
                elif action=='c' or action=='d':
                    pass 
                else:
                    print("That action is not possible. Please try again.")
            else:
                print("Please enter a valid action")
    #draw 2 city cards
    draw_two() #calls resolve_epidemic() and resolve_hand_limit()
    infect()     #infect cities

    #next turn
    if turn==len(players):
        turn = 1 #start the rotation over
    else:
        turn+=1 #else next person
        
    











