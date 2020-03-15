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
                "tasks": []
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

def assign_tasks():
    """ Assign tasks to the members """
    # todo : Essayer qu’une personne ne fasse pas plusieurs tâches d’affilée
    # todo : Essayer d’éviter un maximum qu’une personne fasse plusieurs fois la même tâche
    members = get_members()
    tuple_tasks_occurences = get_tasks_and_occurences()
    periods_info = tuple_tasks_occurences[1]
    tasks = tuple_tasks_occurences[0]
    attributed_tasks = []
    nbTasks = 0

    for period in periods_info:
        temp_task = []
        for task in tasks:
            if period in task["occurence"]:
                temp_members = []

                i = 0
                while i < int(task["person"]):
                    member = random.choice(members)
                    while int(len(member["tasks"]) > nbTasks/int(len(members))):
                        member = random.choice(members)

                    nbTasks += 1
                    members[members.index(member)]["tasks"].append(
                        task["name"])
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
    create_output(attributed_tasks)


assign_tasks()