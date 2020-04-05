import inspect
import random

import const as const
import sys
from kivy import require
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.utils import get_color_from_hex


class Main(App):
    """
    Main class of the GUI app.

    Inheritance: Kivy.app.App
    Version: 1.1.0 (04/04/2020)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = "#3d3d3d"  # Couleur de fond en hex, qui est convertie et chargée plus tard.

        self.title = "CSLabs - Assigneur de tâches"  # Titre de la fenêtre

    def build(self):
        """
        Main function of the GUI app.

        Version: 1.1.0 (04/04/2020)
        """
        self.sm = ScreenManager(transition=SlideTransition())  # TODO: Définir l'animation de transition voulue
        self.members = Members(name="Members")  # Création des menus
        self.tasks = Tasks(name="Tasks")
        self.output = Output(name="Output")

        self.sm.add_widget(self.members)
        self.sm.add_widget(self.tasks)
        self.sm.add_widget(self.output)

        return self.sm


class Members(Screen):
    """
    Members menu.

    Inheritance: Kivy.uix.screenmanager.Screen
    Version: 1.0.0 (03/04/2020)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Tasks(Screen):
    """
    Tasks menu.

    Inheritance: Kivy.uix.screenmanager.Screen
    Version: 1.0.0 (03/04/2020)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Output(Screen):
    """
    Output menu.

    Inheritance: Kivy.uix.screenmanager.Screen
    Version: 1.0.0 (03/04/2020)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


# ====== Logic section ======= #
def create_output(attributed_tasks):
    """ Create the output file to visualize the information """

    # TODO: L’application génère un pdf avec le programme du week-end : pour chaque moment et pour chaque tâche,
    #  qui doit la réaliser

    with open(const.f_path_output, "w") as file_output:
        for period in attributed_tasks:
            file_output.write("==================== " + period["period"].upper() + " ====================\n")
            for task in period["tasks"]:
                file_output.write("Task : " + task["name"] + "\n")
                file_output.write(
                    "Members : " + ", ".join([str(x) for x in task["members"]]) + "\n\n")

        file_output.close()


def get_members():
    """ Returns the member list from the file """
    with open(const.f_path_members, "r") as data_members:
        members = []
        for line in data_members:
            occurrence = []
            member_data = [x.strip() for x in line.split("|")]
            if len(member_data) > 1:
                occurrence = [x.strip() for x in member_data[1].split(",")]
            members.append({
                "name": member_data[0],
                "tasks": [],
                "occurrence": occurrence
            })
        data_members.close()
        return members


def get_tasks_and_occurrences():
    """ Returns the task list from the file """
    with open(const.f_path_tasks, "r") as data_tasks:
        tasks = []
        occurrences = []
        line = [x.strip() for x in data_tasks.readline().split()]
        while line:
            occurrence = [x.strip() for x in data_tasks.readline().split(", ")]
            tasks.append({
                "name": line[0],
                "person": line[1],
                "occurrence": occurrence
            })
            occurrences.extend(occurrence)
            line = [x.strip() for x in data_tasks.readline().split()]
        data_tasks.close()
        return tasks, list(dict.fromkeys(occurrences))


def choose_member(task_name, period, members, member_periods_prec):
    """
    # TODO: Spec
    """
    members_available = members.copy()
    sum_nb_task = 0
    # Supprime les membres qui sont déja affectés à une tache pour la période
    for member in members:
        sum_nb_task += len(member["occurrence"])
        if period in member["occurrence"]:
            members_available.remove(member)
    # Supprime les membres qui sont au dessus de la moyenne de taches affectées
    mean_nb_task = sum_nb_task / len(members)
    members_available_temp = members_available.copy()
    for member_available in members_available_temp:
        if len(member_available["tasks"]) > mean_nb_task:
            members_available.remove(member_available)
    if len(members_available) == 0:
        raise Exception(f"Pas assez de membres pours assigner toutes les taches de la période: {period}")
    # Évite un maximum qu’une personne fasse plusieurs tâches d’affilée si il y a assez de membres
    # Et essayer d’éviter qu’une personne fasse plusieurs fois la même tâche
    members_available_not_in_row = members_available.copy()
    for member_not_in_row in members_available:
        if (member_not_in_row["name"] in member_periods_prec) or (task_name in member_not_in_row["tasks"]):
            members_available_not_in_row.remove(member_not_in_row)

    if len(members_available_not_in_row) == 0:
        return random.choice(members_available)
    else:
        return random.choice(members_available_not_in_row)


def assign_tasks():
    """ Assign tasks to the members """
    members = get_members()
    tuple_tasks_occurrences = get_tasks_and_occurrences()
    periods_info = tuple_tasks_occurrences[1]
    tasks = tuple_tasks_occurrences[0]
    attributed_tasks = []
    member_period_prec = []

    for period in periods_info:
        temp_task = []
        for task in tasks:
            if period in task["occurrence"]:
                temp_members = []
                i = 0
                while i < int(task["person"]):
                    member = choose_member(task["name"], period, members, member_period_prec)
                    members[members.index(member)]["tasks"].append(task["name"])
                    members[members.index(member)]["occurrence"].append(period)
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


if __name__ == "__main__":
    require("1.11.1")  # Version minimale requise
    Config.set('input', 'mouse', 'mouse,disable_multitouch')  # Empêcher la gestion multitouch par défaut de Kivy
    [Builder.load_file("../design/{}.kv".format(menu.lower()))
     for menu, obj in inspect.getmembers(sys.modules[__name__])
     if inspect.isclass(obj) and issubclass(obj, Screen) and menu != "Screen"]  # Énumérer toutes les classes existantes dans ce module, ne prendre que les descendantes de kivy.uix.screenmanager.Screen sauf lui-même et charger le design kv correspondant.
    Window.clearcolor = get_color_from_hex(Main().bg_color)  # Chargement de la couleur de fond

    Main().run()  # Lancement de la GUI
