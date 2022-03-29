# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 20:53:46 2022

@author: Usuario
"""

import csv
from arbol0 import person
with open('Arbol Genealogico.csv','r') as arbol:
    reader = csv.reader(arbol)
    all_data = {}   
    for i,row in enumerate(reader):
        if i !=0:
            try:
                personID=int(row[0])
            except ValueError:
                personID = None
            sex=row[1]            
            nick=row[2]            
            name=row[3]
            last=row[4]
            father={'first':row[5],'last':row[6]}
            mother={'first':row[7],'last':row[8]}            
            middle=row[9]
            last2=row[10]
            try:
                day=int(row[11])
            except ValueError:
                day = None
            try:
                month=int(row[12])
            except ValueError:
                month = None
            try:    
                year=int(row[13])
            except ValueError:
                year = None
            profession=row[14]
            human = person(personID = 'personID', name = '')
            all_data[personID] = person(personID=personID,name=name,nick=nick,\
                                       last= last,last2=last2,sex=sex,\
                                           year=year,month=month,day=day,profession=profession)
            all_data[personID].father = father
            all_data[personID].mother = mother
for ID,human in all_data.items():
    for ID2,possible_parent in all_data.items():
        if type(human.father) == dict:
            if human.father['first'] == possible_parent.name and human.father['last'] == possible_parent.last_name:
                human.assign_father(possible_parent)
        if type(human.mother) == dict: 
            if human.mother['first'] == possible_parent.name and human.mother['last'] == possible_parent.last_name:
                human.assign_mother(possible_parent)
            

    