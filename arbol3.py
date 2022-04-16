# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 20:53:46 2022

@author: Usuario
"""
from arbol_tryout import Person
from arbol_tryout import tree
import csv


def load_csv_tree(arbol_genealogico):
    with open(arbol_genealogico, 'r') as arbol:
        reader = csv.reader(arbol)
        all_data = {}

        for i, row in enumerate(reader):
            if i != 0:
                some_data = False
                for j in row:
                    if j != '':
                        some_data = True
                try:
                    personID = int(row[0])
                except ValueError:
                    personID = None
                if some_data:
                    for j in range(1, 17):  # Sorry about magic number. Number of rows with relevant data.
                        if row[j].strip() == '':
                            row[j] = None
                        elif type(row[j]) == str:
                            row[j] = row[j].strip()
                    sex = row[1]
                    nick = row[2]
                    name = row[3]
                    last = row[4]
                    father = {'first': row[5], 'last': row[6]}
                    try:
                        father['ID'] = int(row[7])
                    except (ValueError,TypeError):
                        father['ID'] = None
                    mother = {'first': row[8], 'last': row[9]}
                    try:
                        mother['ID']= int(row[10])
                    except (ValueError,TypeError):
                        mother['ID']= None
                    middle = row[11]
                    last2 = row[12]
                    try:
                        day = int(row[13])
                    except (ValueError, TypeError):
                        day = None
                    try:
                        month = int(row[14])
                    except (ValueError, TypeError):
                        month = None
                    try:
                        year = int(row[15])
                    except (ValueError, TypeError):
                        year = None
                    profession = row[16]
                    all_data[personID] = Person(personID=personID, name=name, nick=nick, middle=middle,
                                                last=last, last2=last2, sex=sex,
                                                year=year, month=month, day=day, profession=profession)
                    all_data[personID].father = father
                    all_data[personID].mother = mother
    Larroque_Tree = tree(place_name='Larroque')
    same_name_humans = {}
    bad_data = 0

    bad_data_parents = []  # This variable tells us how many people don't have their parents correctly assigned.
    # We need to incorporate all people with the same name to latter assess if they are the correct parent

    for ID, human in all_data.items():
        for ID2, same_name in all_data.items():
            all_same_name = [human]
            if human.name == same_name.name and human.last_name == same_name.last_name and same_name != human:
                all_same_name.append(same_name)
                index = human.name, human.last_name
                same_name_humans[index] = all_same_name

        Larroque_Tree.all_people[ID] = human
    # Then, we assign each human to their parents.
    bad_data_offspring = []
    for ID, human in all_data.items():  # added this line recently. Might have to debug
        for ID2, possible_parent in all_data.items():
            if type(human.father) == dict:
                fathers_name = human.father['first']
                father_last = human.father['last']
                if fathers_name is None and father_last is None:
                    human.father = None
                index = fathers_name, father_last
                if human.father is not None and human.father['first'] == possible_parent.name and human.father[
                    'last'] == possible_parent.last_name:
                    if index in same_name_humans:
                        assigned = False
                        print('Two people with same name')
                        bad_data_offspring.append(human)
                        for same_name_father in same_name_humans[index]:
                            if human.father['ID'] and human.father['ID'] == same_name_father.ID:
                                human.assign_father(same_name_father)
                                print(f'assigning person with ID: {possible_parent.ID} as father of {human.ref}')
                                assigned = True
                                break
                        if not assigned:
                            for same_name_father in same_name_humans[index]:
                                father_info = same_name_father.to_json()
                                Is_father = input(f'Is this {human.ref}\'s father?:{same_name_father.ref}?(Y/N/maybe)')
                                while Is_father == '':
                                    Is_father = input('Is he the father?')
                                if Is_father[0] == 'm' or Is_father[0] == 'M' or Is_father == '':
                                    print(father_info)
                                    Is_father = input('Is he the father?')
                                    while Is_father == '':
                                        Is_father = input('Is he the father')
                                if Is_father[0] == 'Y' or Is_father[0] == 'y':
                                    human.assign_father(same_name_father)
                                    break
                    else:
                        human.assign_father(possible_parent)
            if type(human.mother) == dict:
                mothers_name = human.mother['first']
                mother_last = human.mother['last']
                if mothers_name is None and mother_last is None:
                    human.mother = None
                index = mothers_name, mother_last
                if human.mother is not None and human.mother['first'] == possible_parent.name and human.mother[
                    'last'] == possible_parent.last_name:
                    if index in same_name_humans:
                        assigned = False
                        print('Two people with same name')
                        bad_data_offspring.append(human)
                        for same_name_mother in same_name_humans[index]:
                            if human.mother['ID'] and human.mother['ID'] == same_name_mother.ID:
                                human.assign_mother(same_name_mother)
                                print(f'assigning person with ID: {possible_parent.ID} as mother of {human.ref}')
                                assigned = True
                                break
                        if not assigned:
                            for same_name_mother in same_name_humans[index]:
                                mother_info = same_name_mother.to_json()
                                Is_mother = input(f'Is this {human.ref}\'s mother?:{same_name_mother.ref}?(Y/N/maybe)')
                                while Is_mother == '':
                                    Is_mother = input('Is she the mother?')
                                if Is_mother[0] == 'm' or Is_mother[0] == 'M' or Is_mother == '':
                                    print(mother_info)
                                    Is_mother = input('Is he the mother?')
                                    while Is_mother == '':
                                        Is_mother = input('Is he the mother')
                                if Is_mother[0] == 'Y' or Is_mother[0] == 'y':
                                    human.assign_mother(same_name_mother)
                                    break
                    else:
                        human.assign_mother(possible_parent)

        if type(human.father) == dict:
            print(f'here here here {human.ID}')
            print(
            f'{human.ref}\'s (ID: {human.ID})father\'s name cannot be found in the list. Check for errors')
            bad_data += 1
            bad_data_parents.append(human.father)
        if type(human.mother) == dict:
            print(
               f'{human.ref}\'s (ID: {human.ID}) mother \'s name cannot be found in the list. Check for errors')
            bad_data += 1
            bad_data_parents.append(human.mother)
    print(f'{bad_data} people with bad data parents')


    Larroque_Tree.to_json()
    return Larroque_Tree
