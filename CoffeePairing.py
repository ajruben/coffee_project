import pandas as pd
import csv
import random
import copy
import os



# path to the CSV files with participant data
participants_csv = "random_csv.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Your name:"
header_email = "Your e-mail:"

# path to CSV file that stores conversation starters
conversation_starters_csv = "conversation_starters.csv"

# path to TXT file that stores the pairings of this round
new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

# path to CSV file that stores the pairings of this round
new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_pairs_csv = "Coffee Partner Lottery all pairs.csv"
        
# init set of old pairs
opairs = set()

DELIMITER=','

# load all previous pairings (to avoid redundancies)
if os.path.exists(all_pairs_csv):
    with open(all_pairs_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            opairs.add(tuple(group))
                
# load conversation starters from CSV file
def load_conversation_starters() : 
        starters = {"Random": []}
        if os.path.exists(conversation_starters_csv):
                with open(conversation_starters_csv, "r") as file:
                        csvreader = csv.reader(file, delimiter=DELIMITER)
                        for row in csvreader:
                                starters[row[0]] = row[1:]
        return starters

# pick random conversation starter
def random_conversation_starter(conversation_starters_csv):
        try:
                with open(conversation_starters_csv, "r") as file:
                        csvreader = csv.reader(file, delimiter=DELIMITER)
                        next(csvreader, None) #skip header 
                        
                        #selection of random convesation starter from the first column (for pairs with no similar characteristic)
                        no_sim_char = [row[0] for row in csvreader]
                        #pick a random conversation starter for the pairs
                        random_conversation_starter = random.choice(no_sim_char)
                        return random_conversation_starter
        except FileNotFoundError:
                print("File not found")

# load participant's data
formdata = pd.read_csv('random_csv.csv')

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))

# check if all participants in a group have the same favorite color, season, or city/nature preference
def all_same_property(df, property_column, pair):
    #retrieve the indices of the persons in the paired group
    indices = df[df['Your e-mail:'].isin(pair)].index
    #check their answers for the respective question
    answers = (df[property_column][indices]).tolist()
    #check if their answers are the same
    unique_answers = set(answers)
    #depending if the answer the same for everyone, return True, else return False
    if len(unique_answers) == 1:
        return True
    else:
        return False
# get conversation starter based on a specific property
def get_property_conversation_starter(conversation_starters, property_value):
    return conversation_starters.get(property_value, ["No conversation starter found for this property."])

# try creating new pairing until successful
def FindNewPairs(max_tries=10, group_size=2):
    attempt_number = 1
    new_pairs_found = False # Boolean flag to check if new pairing has been found
    assert len(participants)/group_size > 2 #want at least 2 groups
    
    # init set of new pairs
    npairs = set()
    # running set of participants
    nparticipants = copy.deepcopy(participants)
    
    while not new_pairs_found and attempt_number <= max_tries:   # to do: add a maximum number of tries
        # if odd number of participants and even groupsize, create one group size + 1, then even group size
        
        while (len(nparticipants)%group_size != 0):
            plist=[]
            for i in range(group_size +1):
                p = random.choice(nparticipants)
                plist.append(p)
                nparticipants.remove(p)    
            plist.sort()
            # add alphabetically sorted list to set of pairs
            npairs.add(tuple(plist))

    
        # while still participants left to pair...
  
        while len(nparticipants) > 0:
            plist=[]
            
            for i in range(group_size):
                
                p = random.choice(nparticipants)
                plist.append(p)
                nparticipants.remove(p)

            plist.sort()    
            # add alphabetically sorted list to set of pairs
            npairs.add(tuple(plist))

    
        # check if all new pairs are indeed new, else reset
        if npairs.isdisjoint(opairs):
            new_pairs_found = True
            
        else:
            npairs = set()
            nparticipants = copy.deepcopy(participants)
            attempt_number += 1
    
    return npairs, attempt_number
npairs, attempt_number = FindNewPairs(group_size=3)

# assemble output for printout
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

# load conversation starters
conversation_starters = pd.read_csv('conversation_starters.csv')
for i, pair in enumerate(npairs):
    pair = list(pair)
    gen_pair_string = f"\n* Members of pair number {i +1}: "
    for member in range(len(pair)):
        gen_pair_string += pair[member]
        if member < len(pair) - 2:
            gen_pair_string+= ', '
        elif member == len(pair) -2:
            gen_pair_string+= ', and '
        else:
             gen_pair_string += '.\n'
         
    
    output_string +=  gen_pair_string
    output_string += "Conversation starter: "
    # Checking if all participants in the pair have the same favorite color
    if all_same_property(formdata, 'Your favorite color:', pair):
        color = formdata.loc[formdata[header_email] == pair[0], 'Your favorite color:'].iloc[0]
        color_conversation_starters = conversation_starters[color][0]

        if color_conversation_starters:
            output_string += color_conversation_starters + "\n"
        else:
            output_string += "No conversation starter found for this color.\n"
    
    # Checking if all participants in the pair have the same favorite season
    elif all_same_property(formdata, 'Your favorite season:', pair):
        season = formdata.loc[formdata[header_email] == pair[0], 'Your favorite season:'].iloc[0]
        season_conversation_starters = conversation_starters[season][0]
        #season_conversation_starters = get_property_conversation_starter(conversation_starters, season)
        if season_conversation_starters:
            output_string += season_conversation_starters + "\n"
        else:
            output_string += "No conversation starter found for this season.\n"
    
    # Checking if all participants in the pair have the same preference for city/nature
    elif all_same_property(formdata, 'prefer city or nature:', pair):
        preference = formdata.loc[formdata[header_email] == pair[0], 'prefer city or nature:'].iloc[0]
        preference_conversation_starters = conversation_starters[preference][0]
        #preference_conversation_starters = get_property_conversation_starter(conversation_starters, preference)
        if preference_conversation_starters:
            output_string += preference_conversation_starters + "\n"
        else:
            output_string += "No conversation starter found for this preference.\n"
    
    else:
        # If none of the specific properties match, assign a random conversation starter from the general pool
        output_string += random.choice(conversation_starters["Random"]) + "\n"
    
# write output to console
print(output_string)

# write output into text file for later use
with open(new_pairs_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# write new pairs into CSV file (for e.g. use in MailMerge)
with open(new_pairs_csv, "w") as file:
    header = ["name1", "email1", "name2", "email2", "name3", "email3"]
    file.write(DELIMITER.join(header) + "\n")
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"
            if i < len(pair)-1:
                file.write(name_email_pair + DELIMITER + " ")
            else:
                file.write(name_email_pair + "\n")
                
# append pairs to history file
if os.path.exists(all_pairs_csv):
    mode = "a"
else:
    mode = "w"

with open(all_pairs_csv, mode) as file:
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            if i < len(pair)-1:
                file.write(pair[i] + DELIMITER)
            else:
                file.write(pair[i] + "\n")


             
# print finishing message
print()
print(f"Job done after {attempt_number} attempts.")
