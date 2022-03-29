# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 16:18:59 2022

@author: Usuario
"""


#class tree():
    
from math import inf
#all_ancestors 1 is all the ancestors of person1, all_ancestors2 is all ancestors of person2. 

def relation(person1,person2):
    all_ancestors1 = []
    all_ancestors2 = []
    ancestors1 = {person1}
    ancestors2 = [person2]
    common_ancestors = []
    all_ancestors1.append(ancestors1)
    all_ancestors2.append(ancestors2)
    i = 0
    all_messages = []
    smallest_minimum = inf
    #i is the generation
    while i < len(all_ancestors1) or i < len(all_ancestors2):
        for line in [all_ancestors1,all_ancestors2]:
            prev_gen = []
            if i < len(line):
                for ancestor in line[i]:
                    if ancestor != None:
                        if ancestor.father != None:
                            prev_gen.append(ancestor.father)
                        if ancestor.mother != None:
                            prev_gen.append(ancestor.mother)
                if len(prev_gen) > 0:
                    line.append(prev_gen)
                    names = []
                    for loco in prev_gen:
                        names.append(loco.name + str(i))
                        print(names)
                            
        i += 1
    return all_ancestors1,all_ancestors2
    for i,gen in enumerate(all_ancestors1):
        for human1 in gen:
            for j,gen2 in enumerate(all_ancestors2):
                for human2 in gen2:
                    if human1 == human2:

                        gen_min = min(i,j)
                        gen_max = max(i,j)
                        gen_diff = i-j
                        if gen_min < smallest_minimum:

                            smallest_minimum = gen_min
                        
                        if j >= i:
                            oldest = person1
                            youngest = person2
                        elif j < i:
                            oldest = person2
                            youngest = person1

                        if human1.name != None or human1.last != None:
                            
                            try:
                                common_ancestor = human1.name + ' ' + human1.last
                            except AttributeError:
                                common_ancestor = human1.name
                            except AttributeError:
                                common_ancestor = human1.middle
                            except AttributeError:
                                common_ancestor = human1.nick
                            except AttributeError:
                                common_ancestor = human1.last
                            if gen_min == 0:
                                if gen_diff == 1:
                                    relationship_main = 'parent'
                                elif gen_diff == 2:
                                    relationship_main = 'grand parent'
                                    relationship_main = 'great-' * (gen_diff - 2) + 'grand ' 'parent'
                            elif gen_diff == 0:
                                if gen_min == 1:
                                    relationship_main = 'brother/sister'
                                elif gen_min == 2:
                                    relationship_main = f'{gen_min - 1}º cousin'
                            else:
                                relationship_main = f'{gen_min}º aunt/uncle'
                        else:
                            common_ancestor = 'no name given'
                        message1 = f'common ancestor is {common_ancestor}'
                        message2 = f'he is {i} generations from person1: {str(person1.name)}, and {j} from person2: {str(person2.name)}'
                        if oldest.name != None or youngest.name != None:
                            try:
                                message3 = f'{oldest.name} is {relationship_main} of {youngest.name}'
                            except AttributeError:
                                message3 = f'oldest is {relationship_main} of {youngest.name}'
                            except AttributeError:
                                message3 = f'{oldest.name} is {relationship_main} of youngest'
                        else:
                            message3 = f'oldest is {relationship_main} of youngest'
                        whole_message = f'{message1}\n{message2}\n{message3}'
                        if gen_min <= smallest_minimum:
                            all_messages.append(whole_message)
                        common_ancestors.append(common_ancestor)
    for i,message in enumerate(all_messages):
        print(f'message {i}: {message}\n') 
    return  common_ancestors                          



        
        
        
    