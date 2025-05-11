import random
from src.__init__ import get_file_path, KNOWN_POSITIVE_MESSAGES

last_dk_key = None
coord_range = {"maximum_x": 1000, "maximum_y": 1000}

def get_actions(num_of_actions=None):
    actions = []
    last_action = None
    num_actions = random.randint(5, 8) if num_of_actions is None else num_of_actions
    for _ in range(num_actions):
        action_list = ["dk", "dk_shift", "mm", "mm_dk"]
        if last_action == "mm" and "mm" in action_list:
            action_list.remove("mm")
        weights = [1, 3, 1, 2]
        new_action = random.choices(action_list, weights=weights[:len(action_list)], k=1)[0]
        last_action = new_action
        actions.append(new_action)
    if not any(action in ["dk", "dk_shift"] for action in actions):
        guaranteed_action = random.choice(["dk", "dk_shift"])
        actions.insert(random.randint(0, len(actions)), guaranteed_action)
    return actions

def get_coord(coord_type=None):
    return random.randint(0, coord_range["maximum_x"]) if coord_type == "x" else random.randint(0, coord_range["maximum_y"])

def get_direction():
    global last_dk_key
    keys = ["w", "a", "s", "d"]
    keys.remove(last_dk_key) if last_dk_key != None else ""
    key = random.choice(keys)
    last_dk_key = key
    return key

def get_messages(num=1, use_old_messages=False):
    messages = []
    # Select the positive messages to choose from
    if use_old_messages:
        with open(get_file_path("assets/messages.txt"), 'r') as file:
            positive_messages = [line.strip() for line in file.readlines()]
    else:
        positive_messages = KNOWN_POSITIVE_MESSAGES
    
    # Randomly selected the inputted number of messages
    while len(messages) < num:
        new_message = random.choice(positive_messages)
        if new_message not in messages:
            messages.append(new_message)
    return messages

def get_random_time(start_range=0.3, end_range=0.5):
    return random.uniform(random.uniform(start_range, start_range*random.choice([1.05, 1.1, 1.15, 1.2])), random.uniform(end_range*random.choice([0.5, 0.6, 0.7, 0.8]), end_range))
