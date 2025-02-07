from random import randint, random, choice
import math
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower_alpha="abcdefghijklmnopqrstuvwxyz"

def bool_roll(percent):
    roll1=randint(1,100)
    if roll1<=percent:
        return True
    else:
        return False

def roll():
    return randint(1,100)

# Constants
G = 6.674*(10**(-11))
Stefan_Boltzmann = 5.670*(10**(-8))
AU = 149000000000 # In meters
Sun_Lumin = 3.846*(10**26) # In watts
Sun_Lifetime = 10*10**9 # 10 billion years

# Lists
habitable_zone = ["unset","unset"]
planet_distances = []
planet_sizes = []
planet_sizes_num = []
planet_display_dict = {} # This is what is displayed.
planet_num_dict = {} # This is the actual keeper of info.
star_dict = {}
moon_num_dict = {}
moon_display_dict = {}

united_display_dict = {}

# Geologically Active % - 33% Sample from 4/12 rocky worlds. (Venus, Earth, Io, Triton)
# Magnetic Field % - 50% if Geo Active. Sample from 2/12 rocky worlds. (Ganyemede, Earth)
# Atmosphere % - 90% if Magnetic. 50% if Geologically active. Thin or non-existent if neither.
# Water % - IHZL = Inner Habitable Zone Line. 0% if less than 0.5 IHZL. Follows the
#           Linear equation 0.4x+0.1 relative to the IHZL. (50% at 1). Up until
#           it reaches 90% at 2 IHZL. Multiply by 0.1 if no atmosphere.
# If Geologically Active, has Atmosphere, in habitable zone, and has Water. Flag as habitable.
# (About 8% of rocky worlds in the habitable zone are habitable.)

# If is habitable, roll an 80% chance of it having native life.
# (Life has existed for 4 billion years out of the 4.6 billion years.)

# If it has native life, roll a 50% chance of it having plant life. (40%)
# (Fungi has existed for 2 billion years out of the 4 billion years.)

# If it has plant life, roll a 62.5% chance of it having animal life. (25%)
# (Blatant favoritism here. I just don't want a bunch of worlds with only f---ing plants.)

# If it has animal life, roll a 20% chance of it having intelligent life. (5%)
# (More blatant favoritism. I only have so many worlds to work with.)

# If it has intelligent life, roll a 20% chance of it having civilization. (1%)
# (Yes this is INSANELY optimistic. A whooping 1% of habitable planets having an intelligent
# civilization. But I'm only going to have like 200 stars or so to play with. And I would
# like CoD to encounter aliens before I die of old age writing the lore for 9036 AD.)

def roll_flags(num_dict, display_dict):
    for x in display_dict:
        if num_dict[x]["mass"] <= 54 and num_dict[x]["mass"] >= 5:
            if bool_roll(33): # Has geological activity?
                display_dict[x]["Flags"]+=["Geologically Active"]
                if bool_roll(50): #Has magnetic field?
                    display_dict[x]["Flags"]+=["Magnetic Field"]
                    if bool_roll(90): # Has atmosphere?
                        display_dict[x]["Flags"]+=["Atmosphere"]
                else: # No magnetic field
                    if bool_roll(50): 
                        display_dict[x]["Flags"]+=["Atmosphere"]
            IHZL = habitable_zone[0]
            if num_dict[x]["distance"] > 0.5*IHZL and num_dict[x]["distance"] < 2*IHZL:
                water_roll = bool_roll(round(100*(0.4*num_dict[x]["distance"]+0.1)))
                if (water_roll and
                num_dict[x]["distance"] >= habitable_zone[0] and
                num_dict[x]["distance"] <= habitable_zone[1]):
                    display_dict[x]["Flags"]+=["Liquid Water"]
                elif (water_roll and
                num_dict[x]["distance"] <= habitable_zone[0]):
                    display_dict[x]["Flags"]+=["Water Steam"]
                elif (water_roll and
                num_dict[x]["distance"] >= habitable_zone[1]):
                    display_dict[x]["Flags"]+=["Frozen Water"]
            elif num_dict[x]["distance"] >= 2*IHZL:
                water_roll = bool_roll(90)
                if (water_roll and
                num_dict[x]["distance"] >= habitable_zone[0] and
                num_dict[x]["distance"] <= habitable_zone[1]):
                    display_dict[x]["Flags"]+=["Liquid Water"]
                elif (water_roll and
                num_dict[x]["distance"] <= habitable_zone[0]):
                    display_dict[x]["Flags"]+=["Water Steam"]
                elif (water_roll and
                num_dict[x]["distance"] >= habitable_zone[1]):
                    display_dict[x]["Flags"]+=["Frozen Water"]
            if ("Liquid Water" in display_dict[x]["Flags"] and
            "Geologically Active" in display_dict[x]["Flags"] and
            "Atmosphere" in display_dict[x]["Flags"]):
                display_dict[x]["Flags"]+=["Habitable"]
                life_roll = roll()
                if life_roll == 100:
                    display_dict[x]["Flags"]+=["Advanced Civilization (!!)"]
                elif life_roll >= 95:
                    display_dict[x]["Flags"]+=["Intelligent Life (!)"]
                elif life_roll >= 75:
                    display_dict[x]["Flags"]+=["Animal Life"]
                elif life_roll >= 40:
                    display_dict[x]["Flags"]+=["Plant Life"]
                elif life_roll >= 20:
                    display_dict[x]["Flags"]+=["Microbial Life"]
                
def roll_moons():
    for x in range(len(planet_num_dict)):
        if planet_num_dict[alphabet[x]]["mass"]>=(1/6*100):
            num_moons=min(randint(0,round(planet_num_dict[alphabet[x]]["mass"]/100*6,0)), # Takes the smaller of the two
                          randint(0,round(planet_num_dict[alphabet[x]]["mass"]/100*6,0))) # numbers. Makes it so it's more skewed.
            for y in range(num_moons):
                local_moon_size=min(round(roll()/100*0.5*planet_num_dict[alphabet[x]]["mass"],2),
                                    round(roll()/100*0.5*planet_num_dict[alphabet[x]]["mass"],2),)
                moon_num_dict[alphabet[x]+lower_alpha[y]]={
                    "mass": local_moon_size,
                    "temperature": planet_num_dict[alphabet[x]]["temperature"],
                    "distance": planet_num_dict[alphabet[x]]["distance"]
                }
                moon_display_dict[alphabet[x]+lower_alpha[y]]={
                    "Name": alphabet[x]+lower_alpha[y]+" (Moon)",
                    "Orbiting": planet_display_dict[alphabet[x]],
                    "Mass": return_mass(local_moon_size,"moon"),
                    "Temperature": str(planet_num_dict[alphabet[x]]["temperature"])+" C",
                    "Flags": [],
                    
                }
                
            
def create_star_system():
    global planet_distances
    global planet_sizes
    global planet_num_dict
    global planet_display_dict
    global randomness
    global cull
    global upper_limit
    print()
    jovian_planet_distance = frostline*(1+0.2*random())
    jovian_planet_mass = 66+roll()*0.34
    jov_pos = 0
    planet_distances = [jovian_planet_distance]
    planet_sizes = [return_mass(jovian_planet_mass, "inner")]
    temp_counter = jovian_planet_distance * (1.4+0.6*random())
    while temp_counter <= outer_planet_limit:
        planet_distances = planet_distances+[temp_counter]
        if bool_roll(randomness):
            planet_sizes = planet_sizes+[return_mass(roll(), "outer")]
        else:
            planet_sizes = planet_sizes+[return_mass(44+roll()*(jovian_planet_mass-44)/100, "outer")]
        temp_counter = temp_counter * (1.4+0.6*random())
    temp_counter = jovian_planet_distance / (1.4+0.6*random())
    while temp_counter >= inner_planet_limit:
        planet_distances = [temp_counter]+planet_distances
        if bool_roll(randomness):
            planet_sizes = planet_sizes+[return_mass(roll(), "outer")]
        else:
            planet_sizes = [return_mass(roll()*0.55, "inner")]+planet_sizes
        temp_counter = temp_counter / (1.4+0.6*random())
        jov_pos += 1
    '''
    for x in range(len(planet_distances)-1):
        if (planet_distances[x] != "removed") and (planet_distances[x+1]-planet_distances[x] <= 0.15):
            temprand = randint(1,2)
            if temprand == 1:
                planet_distances[x] = "removed"
            if temprand == 2:
                planet_distances[x+1] = "removed"
    '''
    # This section simply rounds the planet distances. Now removed.
    '''
    for x in range(len(planet_distances)):
        if (planet_distances[x] != "removed"):
            planet_distances[x] = round(planet_distances[x],2)
    '''
    '''
    for x in range(len(planet_distances)):
        try:
            planet_distances.remove("removed")
        except:
            break
    '''
    if cull == True:
        while len(planet_distances) > upper_limit:
            temprand = randint(0,len(planet_distances)-1)
            planet_distances.pop(temprand)
            planet_sizes.pop(temprand)
    print(planet_distances)
    print(planet_sizes)
    for x in range(len(planet_distances)):
        # Template for a planet. I should probably just use an object for this. To hell with it however.
        local_distance = round(planet_distances[x],2)
        local_size = planet_sizes[x]
        local_orbital_period = math.sqrt(planet_distances[x]**3/mass)
        # PLEASE NOTE, the equation is assuming the albedo (reflectiveness) for this is 0.
        # For reference, Earth's is about 0.29.
        local_temperature = ((lumins*Sun_Lumin)/(16*math.pi*
                                     ((local_distance*AU)**2)
                                     *Stefan_Boltzmann))**(1/4)
        planet_display_dict[alphabet[x]] = {
            "Name": alphabet[x],
            "Distance": str(local_distance)+" AU",
            "Orbital Period": str(round(local_orbital_period*365,2))+" days",
            "Temperature": str(round(local_temperature-273,2))+" C", # The 273 is needed to convert from Kelvin to Celsius.
            "Mass": local_size,
            "Flags": [],
        }
        planet_num_dict[alphabet[x]] = {
            "distance": local_distance,
            "orbit": round(local_orbital_period*365,2),
            "temperature": round(local_temperature-273,2), # The 273 is needed to convert from Kelvin to Celsius.
            "mass": planet_sizes_num[x],
        }
        if local_orbital_period*365<37:
            if bool_roll(100-round((local_orbital_period*365/3.6)**2-1,0)):
                planet_display_dict[alphabet[x]]["Flags"] += ["Tidally Locked"]
        if local_distance >= habitable_zone[0] and local_distance <= habitable_zone[1]:
            planet_display_dict[alphabet[x]]["Flags"] += ["In Habitable Zone"]
    if cull == False:
        planet_display_dict[alphabet[jov_pos]]["Flags"] += ["Jovian Anchor Planet"]

def cal_lumins(mass):
    if mass <= 0.43:
        return 0.23*(mass**2.3)
    if mass >= 0.43 and mass <= 2:
        return mass**4
    if mass >= 2 and mass <= 55:
        return 1.4*(mass**3.5)
    if mass >= 55:
        return 32000
    else:
        print("Something went wrong in your lumins function.")

def star_type(mass):
    if mass >= 16:
        return "O Class (Blue Star)"
    if mass >= 2.1:
        return "B Class (Deep Bluish-White Star)"
    if mass >= 1.4:
        return "A Class (Bluish-White Star)"
    if mass >= 1.04:
        return "F Class (White Star)"
    if mass >= 0.8:
        return "G Class (Yellow Star)"
    if mass >= 0.45:
        return "K Class (Orange Star)"
    if mass >= 0.08:
        return "M Class (Red Dwarf)"
    else:
        return "Brown Dwarf"

def return_mass(mass, inner_outer):
    global planet_sizes_num
    mass=round(mass,2)
    if inner_outer == "inner":
        planet_sizes_num = [mass]+planet_sizes_num
    if inner_outer == "outer":
        planet_sizes_num = planet_sizes_num+[mass]
    if mass>=88:
        return "Super Jupiter ("+str(mass)+")"
    elif mass>=77:
        return "Jupiter-like ("+str(mass)+")"
    elif mass>=66:
        return "Sub-Jupiter ("+str(mass)+")"
    elif mass>=55:
        return "Ice Giant ("+str(mass)+")"
    elif mass>=44:
        return "Super Earth ("+str(mass)+")"
    elif mass>=33:
        return "Earth-like ("+str(mass)+")"
    elif mass>=22:
        return "Sub-Earth ("+str(mass)+")"
    elif mass>=11:
        return "Mars-like ("+str(mass)+")"
    elif mass>=1:
        return "Mercury-like ("+str(mass)+")"
    else:
        return "Asteroid ("+str(mass)+")"

def display_dict(dictionary):
    buffer=""
    if "(Moon)" in dictionary["Name"]:
        buffer= "   "
    for x in dictionary:
        if isinstance(dictionary[x], str):
            print(buffer+x+": "+dictionary[x])
        elif isinstance(dictionary[x], list):
            if dictionary[x] != []:
                print(buffer+"Flags:")
                print(buffer+str(dictionary[x]))
    print()

def mySort(e):
    return e[0]

while True:

    habitable_zone = ["unset","unset"]
    planet_distances = []
    planet_sizes = []
    planet_sizes_num = []
    planet_display_dict = {} # This is what is displayed.
    planet_num_dict = {} # This is the actual keeper of info.
    star_dict = {}
    moon_num_dict = {}
    moon_display_dict = {}

    united_display_dict = {}
    
    # All of this taken from Artifexian
    # When in doubt, all units are relative to the Sun,
    # or AUs.
    print("Input Star Name")
    star_name = input(">")
    print("Input Star Mass. (1.0 = The Sun)")
    mass = float(input(">"))
    print("How much randomness would you like? 0 - Classical, 100 - Fully random.")
    print('Input "random" or "r" for this to be random. Integers only please.')
    randomness = input(">")
    if randomness == "random" or randomness == "r":
        randomness = int(roll())
        print(">Random number selected: "+str(randomness))
    else:
        randomness = int(randomness)
    print("Put up an upper limit you would like on the number of worlds. Plus or minus 1. Plus enter to use the default.")
    upper_limit = input(">")
    if upper_limit == "":
        cull = False
    else:
        cull = True
        upper_limit = int(upper_limit)-1+randint(0,2)
    # All of the below are relative to our own Sun, with
    # the Sun at 1.0.
    lumins = cal_lumins(mass)
    diameter = mass**0.74
    star_temp = mass**0.505
    lifetime = mass**-2.5
    star_dict = {
        "Name": star_name,
        "Mass": str(mass)+" Solar Masses",
        "Luminosity": str(round(lumins,2))+" Solar Luminosities",
        "Star Class": star_type(mass),
        "Diameter": str(round(diameter,2))+" Sols",
        "Lifetime": str(round(lifetime*10,2))+" billion years",
    }
    # The following are measured in AU (Distance of Earth
    # to Sun)
    habitable_zone[0] = math.sqrt(lumins)*0.95
    habitable_zone[1] = math.sqrt(lumins)*1.37
    frostline = math.sqrt(lumins)*4.85
    inner_planet_limit = 0.1*mass
    outer_planet_limit = 40*mass
    
    create_star_system()
    
    display_dict(star_dict)

    roll_flags(planet_num_dict,planet_display_dict)
    roll_moons()
    roll_flags(moon_num_dict,moon_display_dict)
    united_display_list=[]
    for x in planet_display_dict:
        united_display_list+=[[x,"planet"]]
    for x in moon_display_dict:
        united_display_list+=[[x,"moon"]]
    united_display_list.sort(key=mySort)
    for x in range(len(united_display_list)):
        if united_display_list[x][1] == "planet":
            united_display_dict[united_display_list[x][0]] = planet_display_dict[united_display_list[x][0]]
        else:
            united_display_dict[united_display_list[x][0]] = moon_display_dict[united_display_list[x][0]]
    for x in united_display_dict:
        display_dict(united_display_dict[x])



    
