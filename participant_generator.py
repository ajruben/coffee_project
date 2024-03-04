import csv
import random
#Requirement 1; not from online form, but this will give us data to work with.

#---------------------------------------------------------------
#Random Participant creater
first_names = ["Olivia", "Emma", "Charlotte", "Amelia", "Sophia", "Isabella",
               "Ava", "Mia", "Evelyn", "Luna", "Liam", "Noah", "Oliver",
               "James", "Elijah", "William", "Henry", "Lucas", "Benjamin",
               "Theodore"]
last_names = ["Jones", "Williams", "Jackson", "Johnson", "Rodriquez", "Smith",
              "Thomas", "Wilson", "Davis", "Garcia", "Thompson", "Martinez",
              "Robinson", "Brown", "Jones", "Miller", "Lopez", "Gonzales",
              "Anderson", "Moore", "Lee", "Perez", "Harris", "Sanchez",
              "Clark", "Ramirez", "Lewis", "Green", "Nelson", "Campbell"]
color_choice = ["Blue", "Red", "Purple"]

random_participants_names = [random.choice(first_names) + " " + random.choice(last_names) for i in range(50)]
random_participants_emails = [] #init empty list

for name in random_participants_names:
    first_name, last_name = name.split()[0].lower(), name.split()[1].lower()
    random_email = first_name + "." + last_name + "@email.com"
    random_participants_emails.append(random_email)
assert len(random_participants_emails) == len(random_participants_names)    

create_csv_format = [["ID", "Your name:", "Your e-mail:", "Your favorite color:"]]

for row in range(len(random_participants_names)):
    create_csv_format.append([row + 1, random_participants_names[row], random_participants_emails[row], random.choice(color_choice)])

with open("random_csv.csv", "w") as file:
    writer = csv.writer(file, lineterminator="\n")
    for line in create_csv_format:
        writer.writerow(line)