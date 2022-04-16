# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 18:46:37 2022

@author: Usuario
"""
from math import inf


def relation(person1, person2):
    all_ancestors1 = {}
    all_ancestors2 = {}
    all_ancestors_global = [all_ancestors1, all_ancestors2]
    all_ancestors1[person1] = {'gen_count': 0, 'line_follower': ''}
    all_ancestors2[person2] = {'gen_count': 0, 'line_follower': ''}
    gen_diff = [inf, inf]
    # i is the generation
    # the while adds the ancestors of previous generations. When the last uploaded
    # ancestor to the tree is added, it won't be able to add another generations
    # (set, and therefore i will be == to all_ancestors, and it will stop the while loop)
    for line in all_ancestors_global:  # line takes on the values: all_ancestors1 and all_ancestors2
        prev_gen = list(line)
        new_gen = []
        gen_count = 1
        another_gen = True
        while another_gen:
            another_gen = False
            for ancestor in prev_gen:  # ancestor first takes on the value of person1, then their parents, and so on.
                if ancestor.father is not None:
                    try:
                        another_gen = True
                        line_follower = line[ancestor]['line_follower']
                        line[
                            ancestor.father] = {'gen_count': gen_count, 'line_follower': (
                                line_follower + 'f')}  # we're counting how many generations away each ancestor is.
                        new_gen.append(
                            ancestor.father)  # new gen is a temporary list only used to explore ancestors
                    except (AttributeError, TypeError):
                        print(
                            f'ancestor has father of type {type(ancestor.father)}. He will not be included in the '
                            f'ancestry')
                if ancestor.mother is not None:
                    try:
                        another_gen = True
                        line_follower = line[ancestor]['line_follower']
                        line[
                            ancestor.mother] = {'gen_count': gen_count,
                                                'line_follower': line_follower + 'm'}  # gencount how many gens from
                        # each ancestor.
                        new_gen.append(
                            ancestor.mother)  # new gen is a temporary list only used to explore ancestors
                    except (AttributeError, TypeError):
                        print(
                            f'ancestor has mother of type {type(ancestor.mother)}. He will not be included in the '
                            f'ancestry')
            prev_gen = list(new_gen)
            new_gen = []
            gen_count += 1
    common_ancestors = set(all_ancestors1).intersection(set(all_ancestors2))
    lca = []
    line_follower_person1 = []
    line_follower_person2 = []
    line_follower_global = [line_follower_person1, line_follower_person2]
    for human in common_ancestors:
        for i, line in enumerate(all_ancestors_global):
            gen_difference = line.get(human)['gen_count']
            if gen_difference < gen_diff[i]:
                gen_diff[i] = gen_difference
                lca = [human]
                line_follower_global[i] = [line.get(human)['line_follower']]
            elif gen_difference == gen_diff[i]:
                line_follower_global[i].append(line.get(human)['line_follower'])
                if human not in lca:
                    lca.append(human)

    if len(lca) > 0:
        message0 = 'The last common ancestor/s is/are'
        for common_ancestor in lca:
            message0 = f'{message0}, {common_ancestor.ref}'
            message1 = f'They are {gen_diff[0]} generations from {person1.ref} and {gen_diff[1]} from {person2.ref}'
            message = f'{message0}\n{message1}'
    else:
        message = f'No common ancestors between {person1.ref} and {person2.ref}'
    print(message)
    return lca, gen_diff[0], gen_diff[1], line_follower_global
