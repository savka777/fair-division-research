# Item names for reference
ITEM_NAMES = [
    "Gaming PC",      # 0
    "MacBook Pro",    # 1 
    "65\" TV",        # 2
    "Sound System",   # 3
    "Coffee Machine", # 4
    "Air Fryer",      # 5
    "Nintendo Switch",# 6
    "Bike",           # 7
    "Leather Couch",  # 8
    "Queen Mattress", # 9
    "Kitchen Knives", # 10
    "Blender",        # 11
    "Desk Chair",     # 12
    "Bookshelf",      # 13
    "Plants"          # 14
]

# Alex (Agent 0): Tech enthusiast - loves gadgets and gaming
# Blake (Agent 1): Comfort lover - wants cozy living items  
# Casey (Agent 2): Fitness & cooking enthusiast - values kitchen/health items
VALUATIONS = [
    # Alex values: Tech > Entertainment > Comfort > Kitchen > Other
    [100, 90, 80, 70, 40,   # Gaming PC, MacBook, TV, Sound System, Coffee Machine
     35, 85, 60, 50, 45,    # Air Fryer, Nintendo Switch, Bike, Leather Couch, Queen Mattress  
     25, 30, 75, 40, 20],   # Kitchen Knives, Blender, Desk Chair, Bookshelf, Plants
    
    # Blake values: Comfort > Entertainment > Kitchen > Tech > Other  
    [70, 60, 95, 80, 65,    # Gaming PC, MacBook, TV, Sound System, Coffee Machine
     45, 55, 30, 100, 90,   # Air Fryer, Nintendo Switch, Bike, Leather Couch, Queen Mattress
     40, 50, 85, 75, 35],   # Kitchen Knives, Blender, Desk Chair, Bookshelf, Plants
    
    # Casey values: Kitchen > Fitness > Comfort > Tech > Entertainment
    [50, 40, 60, 45, 95,    # Gaming PC, MacBook, TV, Sound System, Coffee Machine  
     90, 35, 100, 70, 65,   # Air Fryer, Nintendo Switch, Bike, Leather Couch, Queen Mattress
     85, 80, 55, 50, 75]    # Kitchen Knives, Blender, Desk Chair, Bookshelf, Plants
]

NUM_AGENTS = len(VALUATIONS)
NUM_ITEMS = len(VALUATIONS[0])

# Initial allocation: Give each person their "dream item" to start
# Alex gets Gaming PC, Blake gets Leather Couch, Casey gets Bike
INITIAL_ALLOCATION = [[0], [8], [7]]  

# Alternative interesting starting allocation - potential conflicts
# Alex gets TV (Blake wants it more), Blake gets Gaming PC (Alex wants it more), Casey gets MacBook (not ideal for any)
# INITIAL_ALLOCATION = [[2], [0], [1]]