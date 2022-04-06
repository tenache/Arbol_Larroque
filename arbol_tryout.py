# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:35:30 2022

@author: Usuario
"""
# class Person will have some basic data of the person, such as name, date and place of birth and nickname.
# the assign functions will assign other objects of class Person as father, mother or children. "Children" is a list
# which contains all the persons children.
import json


def tree_from_json(file_name):
    tree = {}
    with open(file_name, 'r') as json_file:
        json_tree = json.load(json_file)
        for key in json_tree:
            json_tree[key] = json.loads(json_tree[key])
    for key in json_tree:
        j_member = json_tree[key]
        personID = j_member['personID']
        j_member['name'] = j_member['name']
        name = j_member['name']
        nick = j_member['nick_name']
        middle = j_member['middle']
        last = j_member['last']
        last2 = j_member['last2']
        sex = j_member['sex']
        year = j_member['year_of_birth']
        month = j_member['month_of_birth']
        day = j_member['day_of_birth']
        profession = j_member['profession']
        Larroque = j_member['lived_in_Larroque?']
        place = j_member['birthplace']
        father = j_member['father']
        mother = j_member['mother']
        children = j_member['children']
        member = Person(name=name, nick=nick, middle=middle, last=last, last2=last2, sex=sex, year=year, \
                        month=month, day=day, profession=profession, place=place, Larroque=Larroque, personID=personID)
        member.father = father
        member.mother = mother
        member.children = children
        tree[key] = member
    for key in tree:
        member = tree[key]
        if member.father != None:
            fatherID = str(member.father)
            father = tree[fatherID]
            member.assign_father(father)
        if member.mother != None:
            motherID = str(member.mother)
            mother = tree[motherID]
            member.assign_mother(mother)
        if member.children:
            offspring = []
            for child in member.children:
                offspring.append(child)
            for childID in offspring:
                if type(childID) == int:
                    child_index = str(childID)
                    child = tree[child_index]
                    member.assign_children(child)
                    member.children.remove(childID)
    return tree


class tree():
    def __init__(self, place_name=None, all_people=None):
        self.place_name = place_name
        if all_people == None:
            self.all_people = {}
        else:
            self.all_people = all_people()

    def to_json(self):
        json_data = {}
        if type(self.all_people) == dict:
            for key in self.all_people:
                new_person_json = self.all_people[key].to_json()
                json_data[key] = new_person_json
        json_data = [json_data]
        file_name = ('tree_' + self.place_name + '.json')
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file)
        print(file_name + ' saved')

    def add_person(self, new_member):
        try:
            new_ID = new_member.ID
            if new_ID in self.all_people.keys():
                new_ID = max(self.all_people.keys()) + 1
            self.all_people[new_ID] = new_member
            new_member.ID = new_ID
        except AttributeError:
            if self.all_people == None:
                new_ID = 1
            else:
                new_ID = max(self.all_people.keys()) + 1
                self.all_people[new_ID] = Person(personID=new_ID, name=new_member)


class Person():
    def __init__(self, personID=None, nick=None, sex=None, name=None, middle=None, last=None, last2=None, year=None,
                 month=None, day=None, place=None, Larroque=True, profession=None):
        self.ID = personID
        self.sex = sex
        self.nick = nick
        self.name = name
        self.middle = middle
        self.last_name = last
        self.birthyear = year
        self.birthmonth = month
        self.birthday = day
        self.birthplace = place
        self.Larroque = Larroque
        self.secondlast = last2
        self.profession = profession
        self.children = []
        self.father = None
        self.mother = None
        self.assign_reference()
        self.no_gender_parent = None

    def assign_reference(self, max_ref_len=10):
        self.ref = ''
        if self.name:
            self.ref = self.ref + self.name
        if self.middle:
            self.ref = self.ref + ' ' + self.middle
        if self.last_name:
            self.ref = self.ref + ' ' + self.last_name
        if len(self.ref) < max_ref_len and self.secondlast:
            self.ref = self.ref + ' ' + self.secondlast
        if len(self.ref) < max_ref_len and self.nick:
            self.ref = self.ref + '(' + self.nick + ')'
        if len(self.ref) < max_ref_len and self.profession:
            self.ref = self.ref + '(profession: ' + self.profession + ')'
        if len(self.ref) < max_ref_len and self.ID:
            self.ref = self.ref + '(ID: ' + str(self.ID) + ')'
        if len(self.ref) < max_ref_len and self.mother:
            self.ref = self.ref + 'son of' + self.mother
        if len(self.ref) < max_ref_len and self.father:
            self.ref = self.ref + 'son of' + self.father

    def assign_father(self, father):
        if type(father) == str:
            self.father = Person (name = father)
        elif type(father) == dict:
            try:
                self.father = Person(name = father['first'], last = father['last'])
            except KeyError:
                return 'Unable to assign father. Wrong type of dict'
        elif type(father) == int:
            self.father = Person(personID = father)
        else:
            self.father = father
        try:
            if self not in father.children:
                father.children.append(self)
        except AttributeError:
            return f'Father assigned, but type is {type(father)}'

    def assign_mother(self, mother):
        if type(mother) == str:
            self.mother = Person(name = mother)
        elif type(mother) == dict:
            try:
                self.mother = Person (name = mother['name'],last=mother['last'])
            except AttributeError:
                return 'Unable to assign mother. Wrong type of dict'
        elif type(mother) == int:
            self.mother = Person(personID = mother)
        else:
            self.mother = mother
        try:
            if self not in mother.children:
                mother.children.append(self)
        except AttributeError:
            return f'Mother assigned, but type is {type(mother)}'

     def assign_children(self, children):
        if type(children) != str:
            if type(children) == str or type(children) == int:
                children = [children]
            else:
                return f'Children must be str or list'
            for i, child in enumerate(children):
                if type(child) == str:
                    self.children.append(Person(name=child))
                elif child == int:
                    self.children.append(Person(personID=child))
                else:
                    self.children.append(child)
                    if self.sex == None:
                        child.no_gender_parent = self
                    elif self.sex[0] == 'm' or self.sex[0] == 'M':
                        if child.father == None:
                            child.father = self
                        else:
                            try:
                                prev_father = child.father
                                child.father = self
                            except AttributeError:
                                print('child assigned is not of type Person')
                            try:
                                if prev_father.children != None:
                                    if child in prev_father.children:
                                        prev_father.remove(child)
                            except AttributeError:
                                print('Previous father not of type Person')
                            print ('Reassignment of father')
                    elif self.sex[0] == 'f' or self.sex[0] == 'F':
                        if child.mother == None:
                            child.mother = self
                        else:
                            try:
                                prev_mother = child.mother
                                child.mother = self
                            except AttributeError:
                                print('child assigned is not of type Person')
                            try:
                                if prev_mother.children != None:
                                    if child in prev_mother.children:
                                        prev_mother.remove(child)
                            except AttributeError:
                                print('Previous mother not of type Person')
                            print ('Reassignment of mother')
    def to_json(self):
        children = []
        children_names = []
        if isinstance(self.mother, Person):
            motherID = self.mother.ID
            mother_name = self.mother.ref
        else:
            motherID = None
            mother_name = None
        if isinstance(self.father, Person):
            fatherID = self.father.ID
            father_name = self.father.ref
        else:
            fatherID = None
            father_name = None
        for child in self.children:
            children.append(child.ID)
            children_names.append(child.ref)
        data = [{
            'personID': self.ID,
            'name': self.name,
            'nick_name': self.nick,
            'middle': self.middle,
            'last': self.last_name,
            'last2': self.secondlast,
            'sex': self.sex,
            'year_of_birth': self.birthyear,
            'month_of_birth': self.birthmonth,
            'day_of_birth': self.birthday,
            'profession': self.profession,
            'mother': motherID,
            'father': fatherID,
            'children': children,
            'children_names': children_names,
            'lived_in_Larroque?': self.Larroque,
            'birthplace': self.birthplace,
            'father_name': father_name,
            'mother_name': mother_name
        }]
        ref = self.ref.replace(' ', '_')
        file_name = (ref + '_' + str(self.ID) + '.json')
        with open(file_name, 'w') as write_file:
            person_json = json.dumps(data, indent=4)
            json.dump(data, write_file, indent=4)

        return person_json


Enzo: Person = Person(name='Enzo', nick='pelado', personID=1, last='DeLuca', sex='male', profession='geologo')
Bruno = Person(name='Bruno', profession='finca', sex='male', last='DeLuca', personID=2)
Gri = Person(name='Gri', profession='bio', sex='female', personID=3, last='Fiorotto')
Franco = Person(personID=4, name='Franco', last='DeLuca', sex='male', profession='finquero')
Giorgio = Person(personID=5, name='Giorgio', last='DeLuca', sex='male')
Guido = Person(personID=6, name='Guido', last='DeLuca', sex='male', profession='finquero', nick='Enzo de Sabri')
Silvia = Person(name='Silvia', last='Dezan', sex='female', personID=7)
Lucia = Person(name='Lucia', last='DeLuca', sex='female', personID=8)
Toto = Person(name='Atilio', middle='F', last='Fiorotto', nick='Toto', sex='m', personID=9)
Palma = Person(name='Palma', last='Fracarolli', sex='female', personID=10)
Gerardo = Person(name='Gerardo', last='Fiorotto', sex='male', personID=11)
Olga = Person(name='Olga', sex='female', personID=12)
Laura = Person(name='Laura', last='Fiorotto', sex='female', personID=13)
Constantino = Person(name='Constantino', last='Fiorotto', sex='male', personID=14)

save_the_people = [Enzo, Bruno, Gri, Franco, Giorgio, Guido, Silvia, Lucia, Toto, Palma,
                   Gerardo, Olga, Laura, Constantino]
Toto.assign_father(Constantino)
Laura.assign_father(Gerardo)
Laura.assign_mother(Olga)
Gerardo.assign_father(Toto)
Olga.assign_mother(Palma)
Gri.assign_father(Toto)
Gri.assign_mother(Palma)
Lucia.assign_father(Franco)
Lucia.assign_mother(Silvia)
Bruno.assign_mother(Silvia)
Guido.assign_father(Bruno)
Guido.assign_mother(Gri)
Enzo.assign_father(Bruno)
Enzo.assign_mother(Gri)
Bruno.assign_father(Franco)
Franco.assign_father(Giorgio)

Tree = tree(place_name='Larroque')
for branch in save_the_people:
    Tree.add_person(branch)

Tree.to_json()
