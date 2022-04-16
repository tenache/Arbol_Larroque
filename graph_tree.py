from arbol2 import relation


# this function will graph two people, and all their ascendants, up to the level of the common ancestor. The program
# will draw special edges marking the path from each person towards the ancestor/s.
# The result will be a .dot file, which will be read by neato to produce a png with the family tree.


def to_graphic_tree(person1, person2):
    print('made it this far')
    people = [person1, person2]
    human = person1
    lca, gen_diff_person1, gen_diff_person2, line_follower_global = relation(person1, person2)
    print('made it this far2')
    print('checkpoint3')
    base_width_for_couple = 6   # the min number of places needed for two people is about 6.
    gen_diffs = [gen_diff_person1, gen_diff_person2]  # how many generations away each person is from lca.
    max_width1 = 2 ** (gen_diffs[0] - 1) * base_width_for_couple
    max_width2 = 2 ** (gen_diffs[1] - 1) * base_width_for_couple
    max_widths = [max_width1, max_width2]
    all_nodes = []
    left_right = [1, -1]  # this is to define positions. Mothers will be graphed on the left (x pos of child - certain
    # amount ) , while fathers will be graphed on right (x pos of child + certain amount)
    edges = []
    to_lca_person1 = []
    to_lca_person2 = []
    to_lca_people = [to_lca_person1, to_lca_person2]
    flipping_parents_person1 = []
    flipping_parents_person2 = []
    flipping_parents = [flipping_parents_person1, flipping_parents_person2]
    connector_nodes = []
    people_with_unknown_fathers = []
    people_with_unknown_mothers = []
    colors = ['#e1a6e1', '#934662', '#e9e2d0']
    # to_lca_people will hold all ancestors which are in direct line with the common ancestor/s
    for i, human in enumerate(people):
        for follower_human in line_follower_global:
            ancestor = human
            for follower_ancestor in follower_human[0]:
                if follower_ancestor == 'f':
                    next_in_line = ancestor.father
                    next_flipper = ancestor.mother
                elif follower_ancestor == 'm':
                    next_in_line = ancestor.mother
                    next_flipper = ancestor.father
                else:
                    print('There was a problem. Things might not look pretty')
                    print(f'follower_human is {follower_human}')
                    print(f'follower_ancestor is {follower_ancestor}')
                ancestor = next_in_line
                to_lca_people[i].append(next_in_line)
                flipping_parents[i].append(next_flipper)


    print('checkpoint4')

    x = 0
    base_x = 0
    for i, human in enumerate(people):
        print('more checkpoints')
        next_gen = True
        gen = 0
        gen_people = 2 ** gen
        gen_width_unit = max_widths[i] / (gen_people * 2)
        print(f'x before reassignment is {x}')
        x = base_x + gen_width_unit * 2
        base_x = x
        print(f'gen_width_unit={gen_width_unit} for {people[i].ref}')
        print(f'x={x}')
        y = 0
        node_name = human.name + '_' + str(human.ID)
        color = '#e5edc4'
        new_node = {'node_name': node_name, 'pos': {'x': x, 'y': y}, 'color': color, 'human': human}
        new_nodes = [new_node]
        all_nodes.append(new_node)
        unknownID = 0
        # this loop goes through each generation and makes a node (i.e., a dictionary for every human). Also, there is
        # a list that holds all the edges, or connections between nodes.
        while next_gen:
            next_gen = False
            gen += 1
            next_new_nodes = []
            for node in new_nodes:
                node_name = node['node_name'] + '_connector'
                style = 'invisible'
                shape = 'circle'
                label = ''
                height = '0.001'
                width = '0.001'
                x = node['pos']['x']
                y = node['pos']['y'] + 1
                connector_node = {'node_name': node_name, 'style': style, 'label': label, 'height': height,
                                  'width': width, 'shape': shape, 'pos': {'x': x, 'y': y }}
                connector_nodes.append(connector_node)
                edges.append(f"{connector_node['node_name']} -- {node['node_name']}")
                if node['human'] is not None:
                    for j, parent in enumerate([node['human'].father, node['human'].mother]):
                        try:
                            if parent.father is not None:
                                next_gen = True
                        except AttributeError:
                            people_with_unknown_fathers.append(node['human'])
                            try:
                                if parent.mother is not None:
                                    next_gen = True
                            except AttributeError:
                                people_with_unknown_mothers.append(node['human'])
                        gen_people = 2 ** gen
                        gen_width_unit = max_widths[i] / (gen_people + 1)
                        if parent in to_lca_people[i]:  # common ancestor must always be in the middle.
                            direction = left_right[i]
                        if parent in flipping_parents[i]:
                            direction = left_right[i] * (-1)  #opposite direction of parent in common ancestor line.
                        else:
                            direction = left_right[j]
                        x = node['pos']['x'] + gen_width_unit * direction
                        y = gen
                        node_human = parent
                        try:
                            node_name = parent.name + '_' + str(parent.ID)
                            color = colors[j]
                        except AttributeError:
                            unknownID +=1
                            node_name = 'Unknown' + '_' + str(gen)+'_'+str(j) + '_' + str(unknownID)
                            color = colors[2]
                        new_node = {'node_name': node_name, 'pos': {'x': x, 'y': y}, 'color': color, 'human': node_human}
                        next_new_nodes.append(new_node)
                        edges.append(f"{new_node['node_name']} -- {connector_node['node_name']}")
            new_nodes = next_new_nodes
            for node in new_nodes:
                all_nodes.append(node)
    print('checkpoint5')
    to_dot_file = '''
    graph dotSrc {
   graph [overlap = "false"]
   node [style=filled, shape = box]
   '''
    for node in all_nodes:
        new_node_str = f"{node['node_name']} [fillcolor=\"{node['color']}\"" \
                       f",pos=\"{str(node['pos']['x'])}," \
                       f"{str(node['pos']['y'])}!\"]"
        to_dot_file += f"\n    {new_node_str}"
    for connector in connector_nodes:
        new_connector_str = f"{connector['node_name']} " \
                            f"[style=invisible,shape=circle,label= \"\",height=0.0001,width=0.0001," \
                            f"pos=\"{connector['pos']['x']},{connector['pos']['y']}!\"]"
        to_dot_file += f"\n     {new_connector_str}"
    for edge in edges:
        to_dot_file += f"\n     {edge}"
    to_dot_file += '\n }'
    print('made it this far3')
    with open('tree_graph.dot', 'w') as tree_graph:
        tree_graph.write(to_dot_file)


