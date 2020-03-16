import random
import const


def create_output(attributed_tasks):
    """ Create the output file to visualize the information """
    # todo : L’application génère un pdf avec le programme du week-end : pour chaque moment et pour chaque tâche, qui doit la réaliser
    with open(const.f_path_output, "w") as file_output:
        for period in attributed_tasks:
            file_output.write("==================== " +
                              period["period"].upper() + " ====================\n")
            for task in period["tasks"]:
                file_output.write("Task : " + task["name"] + "\n")
                file_output.write(
                    "Members : " + ", ".join([str(x) for x in task["members"]]) + "\n\n")

        file_output.close()


def get_members():
    """ Returns the member list from the file """
    with open(const.f_path_members, "r") as data_members:
        temp_members = [x.strip() for x in data_members.readlines()]
        members = []
        for member in temp_members:
            members.append({
                "name": member,
                "tasks": [],
                "occurence":[]
            })
        data_members.close()
        return members


def get_tasks_and_occurences():
    """ Returns the task list from the file """
    with open(const.f_path_tasks, "r") as data_tasks:
        tasks = []
        occurences = []
        line = [x.strip() for x in data_tasks.readline().split()]
        while line:
            occurence = [x.strip() for x in data_tasks.readline().split(", ")]
            tasks.append({
                "name": line[0],
                "person": line[1],
                "occurence": occurence
            })
            occurences.extend(occurence)
            line = [x.strip() for x in data_tasks.readline().split()]
        data_tasks.close()
        return (tasks,list(dict.fromkeys(occurences)))

def choose_member(task_name,period,members,member_periods_prec):
    members_available = members.copy()
    sum_nbTask = 0
    # Supprime les membres qui sont déja affectés à une tache pour la période
    for member in members:
        sum_nbTask += len(member["tasks"])
        if(period in member["occurence"]):
            members_available.remove(member)
    # Supprime les membres qui sont au dessus de la moyenne de taches affectées
    mean_nbTask = sum_nbTask / len(members)
    members_available_temp = members_available.copy()
    for member_available in members_available_temp:
        if((len(member_available["tasks"]) > mean_nbTask)):
            members_available.remove(member_available)
    # Evite;un maximum qu’une personne fasse plusieurs tâches d’affilée si il y a assez de membres
    # Et essayer d’éviter qu’une personne fasse plusieurs fois la même tâche
    members_available_not_in_row = members_available.copy()
    for member_not_in_row in members_available:
        if(member_not_in_row["name"] in member_periods_prec) or (task_name in member_available["tasks"]):
            members_available_not_in_row.remove(member_not_in_row)
    
    if(len (members_available_not_in_row) == 0):
        return random.choice(members_available)
    else:
        return random.choice(members_available_not_in_row)
    

def assign_tasks():
    """ Assign tasks to the members """
    members = get_members()
    tuple_tasks_occurences = get_tasks_and_occurences()
    periods_info = tuple_tasks_occurences[1]
    tasks = tuple_tasks_occurences[0]
    attributed_tasks = []
    member_period_prec = []

    for period in periods_info:
        temp_task = []
        for task in tasks:
            if period in task["occurence"]:
                temp_members = []
                i = 0
                while i < int(task["person"]):
                    member = choose_member(task["name"],period,members,member_period_prec)
                    members[members.index(member)]["tasks"].append(
                        task["name"])
                    members[members.index(member)]["occurence"].append(
                        period)
                    temp_members.append(member["name"])
                    i += 1
                temp_task.append({
                    "name": task["name"],
                    "members": temp_members
                })
        attributed_tasks.append({
            "period": period,
            "tasks": temp_task
        })
        member_period_prec = []
        for person in temp_task:
            member_period_prec.extend(person["members"])
    create_output(attributed_tasks)

assign_tasks()