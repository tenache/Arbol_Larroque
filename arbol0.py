# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:35:30 2022

@author: Usuario
"""
#class person will have some basic data of the person, such as name, date and place of birth and nickname. 
#the assign functions will assign other objects of class person as father, mother or children. "Children" is a list
#which contains all the persons children. 
import json
from arbol1 import relation

def relationship(human1,human2,spanish = False):
  human = human1
  other_human = human2
  generations = 0
  checked_daddies = []
  checked_mommas = []
  while human.father != None:
      if generations > 1000000:
          return ('infinite while loop (first)')
      other_human = human2
      #print(f'generations: {generations}')
      generations += 1
      other_generations = 0
      if human.father == human2 or human.mother == human2:
          message = (f'direct ancestor. {generations} generations apart')
          message_s = ('ancestro directo. {generations} generations de distancia')
          if spanish == True:
              return message_s
          else:
              return message
      print(human.name)
      while other_human.father != None:
          if other_generations > 100000:
              return ('infinite while loop (2nd)')
          print(other_generations)
          print(other_human.father.name)
          print(human.name)

          #print(f'{other_generations}')
          if human == other_human.father:
              #print('second if was true')
              if human.name != None and human.last_name != None:
                  ancestor_name = human.name + '  ' + human.last_name
              else:
                  ancestor_name = 'unknown name'
              message = (f'You share an ancestor: {ancestor_name}, {generations} \
                         generations apart for first person, {other_generations} for the second person  ')
              message_s = (f'Comparten ancestro: {ancestor_name}, a {generations} generaciones\
                           de distancia para la primera persona, y a {other_generations} generacion/es de distancia para la segunda' )
              if spanish == True:
                  return message_s
             
              else:
                  return message
          else:
              other_human = other_human.father
              other_generations += 1 
      else:
          human = human.father
  

def tree_from_json(file_name):
    tree = {}
    with open(file_name, 'r') as json_file:
        json_tree = json.load(json_file)
        for key in json_tree:
            json_tree[key] = json.loads(json_tree[key])
    for key in json_tree:
         j_member = json_tree[key]
         personID = j_member['personID']
         name = j_member['name'],
         nick= j_member['nick_name']
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
         member = person(name = name, nick = nick, middle = middle, last = last, last2 = last2, sex = sex, year = year,\
                         month=month,day=day,profession=profession, place = place, Larroque=Larroque,personID = personID)
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
    def __init__(self, place_name = None, all_people = None):
        self.place_name = place_name
        if all_people == None:
            self.all_people = {}
        else:
            self.all_people = all_people()
    def to_json(self):
        json_data = {}
        if type (self.all_people) == dict:
            for key in  self.all_people:
                new_person_json = self.all_people[key].to_json()
                json_data[key] = new_person_json
        file_name = ('tree_' + self.place_name + '.json' )
        with open(file_name, 'w') as json_file:
            json.dump(json_data,json_file)
        print(file_name + ' saved')
    def add_person(self, new_member):
           try:
               new_ID = new_member.ID
               if new_ID in self.all_people.keys():
                   new_ID = max(self.all_people.keys()) + 1
               self.all_people[new_ID] = new_member
               new_member.ID = new_ID
           except AttributeError :
               if self.all_people == None:
                   new_ID = 1
               else:
                   new_ID = max(self.all_people.keys()) + 1
                   self.all_people[new_ID] = person(personID = new_ID, name = new_member)
                  

class person():
    def __init__(self,personID = None, nick = None, sex = None, name = None, middle = None, last = None, last2 = None, year = None, month = None, day = None, place = None, Larroque = True, profession = None):
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
    def assign_reference(self, max_ref_len = 10):
            self.ref = ''
            if self.name:
                self.ref = self.ref +  self.name
            if self.middle:
                self.ref = self.ref + ' ' + self.middle
            if self.last_name:
                self.ref = self.ref + ' ' +self.last_name
            if len(self.ref) < max_ref_len and self.secondlast:
                self.ref = self.ref + ' ' + self.secondlast
            if len(self.ref) < max_ref_len and self.nick:
                self.ref = self.ref + '(' + self.nick + ')'
            if len(self.ref) <  max_ref_len and self.profession:
                self.ref = self.ref + '(profession: ' + self.profession + ')'
            if len(self.ref) < max_ref_len and self.ID:
                self.ref = self.ref + '(ID: ' + str(self.ID) + ')'
            if len(self.ref) < max_ref_len and self.mother:
                self.ref = self.ref + 'son of' + self.mother
            if len(self.ref) < max_ref_len and self.father:
                self.ref = self.ref + 'son of' + self.father  
      
    def assign_father(self,father):
        if isinstance(father, person):
            self.father = father 
            if self not in father.children:
                father.children.append(self)
        elif type(father) == str:
            self.father = person(name = father)
            # nick = input('cómo le decian? ')
            # name = input('nombre? ')
            # middle = input("segundo nombre? ")
            # last = input('apellido? ')
            # last2 = input("segundo apellido? ")
            # year = input("en que año nació? ")
            # month = input("en qué mes nació? ")
            # day = input("en qué día nació? ")
            # place = input("dónde nació?")
    def assign_mother(self,mother):
        if isinstance(mother,person):
            self.mother = mother
            if self not in mother.children:
                mother.children.append(self)
        elif type(mother) == str:
            self.mother = person(name = mother)
            
    def assign_children(self,children):
        if type(children) != list:
            children = [children]
            for i,child in enumerate(children):
                if isinstance(child,person):
                    self.children.append(child)
                    if self.sex[0] == 'm' or self.sex == 'M':
                        if child.father == None:
                                child.father = self
                    else: 
                        if child.mother == None:
                            child.mother = self
                elif type(child) == str:
                    self.children.append(person(name = child))
    def basic_info(self):
        for attribute in dir(self):
            print(attribute)
    def to_json(self):
        children = []
        if self.mother != None:
            motherID = self.mother.ID
        else:
            motherID = None
        if self.father != None:
            fatherID = self.father.ID
        else:
            fatherID = None
        for child in self.children:
            children.append(child.ID)
        data = {
            'personID':self.ID,
            'name':self.name,
            'nick_name':self.nick,
            'middle':self.middle,
            'last':self.last_name,
            'last2':self.secondlast,
            'sex':self.sex,
            'year_of_birth':self.birthyear,
            'month_of_birth':self.birthmonth,
            'day_of_birth':self.birthday,
            'profession':self.profession,
            'mother':motherID,
            'father':fatherID,
            'children':children,
            'lived_in_Larroque?':self.Larroque,
            'birthplace':self.birthplace,
            }
        ref = self.ref.replace(' ','_')
        file_name = (ref  + '_' + str(self.ID) + '.json')
        print(file_name)
        with open(file_name, 'w') as write_file:
            person_json = json.dumps(data)
            json.dump(data,write_file)
        return person_json


          
Enzo = person(name = 'Enzo', nick='pelado',personID = 1, last = 'DeLuca',sex = 'male',profession = 'geologo')
Bruno = person(name = 'Bruno',profession ='finca',sex='male',last ='DeLuca', personID = 2)        
Gri = person (name = 'Gri', profession = 'bio',sex='female',personID = 3, last = 'Fiorotto')
Franco = person(personID = 4, name = 'Franco', last = 'DeLuca',sex= 'male',profession='finquero')
Giorgio = person(personID = 5, name='Giorgio',last='DeLuca',sex='male')
Guido = person(personID = 6, name ='Guido',last = 'DeLuca', sex = 'male',profession = 'finquero',\
               nick='Enzo de Sabri')
Silvia = person(name = 'Silvia',last='Dezan',sex='female',personID=7)
Lucia = person(name = 'Lucia',last = 'DeLuca',sex = 'female',personID = 8)
Toto = person(name = 'Atilio', middle = 'F', last = 'Fiorotto', nick = 'Toto', \
              sex = 'm',personID = 9)
Palma = person(name = 'Palma', last = 'Fracarolli', sex= 'female',personID =10)
Gerardo = person(name='Gerardo', last='Fiorotto',sex='male',personID=11)
Olga = person (name='Olga',sex='female',personID=12)
Laura = person(name='Laura',last='Fiorotto',sex='female',personID=13)
Constantino = person(name = 'Constantino', last = 'Fiorotto',sex = 'male',personID = 14)

save_the_people = [Enzo,Bruno,Gri,Franco,Giorgio,Guido,Silvia,Lucia,Toto,Palma,\
                   Gerardo,Olga,Laura,Constantino]
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

tree = tree(place_name= 'Larroque')
for branch in save_the_people:
    tree.add_person(branch)
    
tree.to_json()



                      
        