# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 18:46:37 2022

@author: Usuario
"""
from math import inf
from arbol0 import Person
from arbol0 import Enzo

Enzo2 = Person(name='Enzo', nick='con pelo')
Type = type(Enzo2)
print(
    f'are id(type(Enzo)) ({id(type(Enzo))}), imported form arbol0 and id(type(Enzo2))({id(type(Enzo2))}),instanciated in this file, equal?')


def relation(person1, person2):
    print('This line')
    print(f'id Enzo pelado is {id(person1)}, id hairy Enzo is {id(Enzo2)}')
    print(str(type(person1)) + ' type Person1 (Enzo pelado)')
    print(str(type(person1) == Type) + ' isinstance result')
    print(str(type(Enzo2)) + ' type Enzo2, defined in this script')
    print(str(type(Enzo2) == Type) + ' isinstance result for hairy Enzo')
    print(f'are {id(type(Enzo2))} and {id(type(person1))}  equal ?  ' + str(type(person1) == type(Enzo2)))
    all_ancestors1 = {}
    all_ancestors2 = {}
    ancestors1 = {person1: 0}
    ancestors2 = {person2: 0}
    all_ancestors_global = [all_ancestors1, all_ancestors2]
    common_ancestors = []
    all_ancestors1[person1] = 0
    all_ancestors2[person2] = 0
    gen_diff = [inf, inf]
    lca = False
    # i is the generation
    # the while adds the ancestors of previous generations. When the last uploaded
    # ancestor to the tree is added, it won't be able to add another generations
    # (set, and therefore i will be == to all_ancestors, and it will stop the while loop)
    for line in all_ancestors_global:
        prev_gen = list(line)
        new_gen = []
        gen_count = 1
        another_gen = True
        while another_gen == True:
            another_gen = False
            for ancestor in prev_gen:
                if ancestor != None:
                    if isinstance(ancestor.father, Person):
                        print(ancestor.name)
                        another_gen = True
                        gen_count = gen_count
                        line[ancestor.father] = gen_count
                        new_gen.append(ancestor.father)
                    if isinstance(ancestor.mother, Person):
                        another_gen = True
                        gen_count = gen_count
                        line[ancestor.mother] = gen_count
                        new_gen.append(ancestor.mother)
            prev_gen = list(new_gen)
            new_gen = []
            gen_count += 1
    common_ancestors = set(all_ancestors1).intersection(set(all_ancestors2))
    print(all_ancestors1)
    print(all_ancestors2)
    lca = []
    for human in common_ancestors:
        for i, line in enumerate(all_ancestors_global):
            print(lca)
            gen_difference = line.get(human)
            if gen_difference < gen_diff[i]:
                gen_diff[i] = gen_difference
                lca = [human]
            elif gen_difference == gen_diff[i]:
                if human not in lca:
                    lca.append(human)

    if lca:
        message0 = 'The last common ancestor/s is/are'
        for common_ancestor in lca:
            message0 = f'{message0}, {common_ancestor.ref}'
        message1 = f'They are {gen_diff[0]} generations from {person1.ref} and {gen_diff[1]} from {person2.ref}'
        message = f'{message0}\n{message1}'
    else:
        message = f'No common ancestors between {person1.ref} and {person2.ref}'
    print(message)
    return lca
