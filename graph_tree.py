from arbol2 import relation


# this function will graph two people, and all their ascendants, up to the level of the common ancestor. The program
# will draw special edges marking the path from each person towards the ancestor/s.
# The result will be a .dot file, which will be read by neato to produce a png with the family tree.


def to_graphic_tree(person1, person2):
    print('made it this far')
    people = [person1, person2]
    lca, gen_diff_person1, gen_diff_person2, line_follower_global = relation(person1, person2)
    print('made it this far2')
    print('checkpoint3')
    base_width_for_couple = 4  # the min number of places needed for two people is about 6.
    gen_diffs = [gen_diff_person1, gen_diff_person2]  # how many generations away each person is from lca.
    max_width1 = 2 ** (gen_diffs[0] - 1) * base_width_for_couple  # max_width1 is the middle, as person1 is left.
    max_width2 = 2 ** (gen_diffs[1] - 1) * base_width_for_couple  # max width each person and their ascendancy occupy
    max_widths = [max_width1, max_width2]
    all_nodes = []
    left_right = [1, -1]  # this is to define positions. Mothers will be graphed on the left (x pos of child - certain
    # amount ) , while fathers will be graphed on right (x pos of child + certain amount)
    edges = []
    to_lca_person1 = []
    to_lca_person2 = []
    to_lca_people = [to_lca_person1, to_lca_person2]  # people in direct line from a person to an lca.
    flipping_parents_person1 = []
    flipping_parents_person2 = []
    flipping_parents = [flipping_parents_person1, flipping_parents_person2]  # spouse of those in direct line with lca.
    connector_nodes = []  # put there just to make the tree look pretty.
    people_with_unknown_fathers = []
    people_with_unknown_mothers = []
    colors = ['#e1a6e1', '#934662', '#e9e2d0']
    # to_lca_people will hold all ancestors which are in direct line with the common ancestor/s
    # line_follower_global = [['mf', 'mm'], ['ff', 'fm']]
    # this loop generates a list for each person, containing all the humans who are in direct line with lca.
    for i, human in enumerate(people):  # human takes on the value of each person
        # line takes on the value of the sequence (mother or father) needed to follow a person to the ancestor.
        for line in line_follower_global[i]:
            ancestor = human
            for follower in line:  # follower takes on the value: is the next person in line the mother or father?
                if follower == 'f':
                    next_in_line = ancestor.father
                    next_flipper = ancestor.mother
                elif follower == 'm':
                    next_in_line = ancestor.mother
                    next_flipper = ancestor.father
                else:
                    print('A key ancestor is missing. Things might not look pretty')
                    print(f'line is {line}')
                    print(f'follower is {follower}')
                    break
                ancestor = next_in_line
                if next_in_line not in to_lca_people[i]:
                    to_lca_people[i].append(next_in_line)
                if next_flipper not in flipping_parents[i] and next_flipper not in to_lca_people[i]:
                    flipping_parents[i].append(next_flipper)
    for parent_line in flipping_parents:
        for i, parent in enumerate(parent_line):
            if parent in to_lca_people[i]:
                parent_line.remove(parent)

    print('checkpoint4')

    x = 0
    initial_separation = base_width_for_couple / 4  # separation in graph between person1 and person2
    initial_width = 0  # will take on different value for person2.
    middle = max_width1 + initial_separation  # middle will be necessary to place lca.
    # this loop generates the "nodes" with the necessary information to later create the .dot file.
    for i, human in enumerate(people):
        # first we generate the first nodes, then sequentially fill up the ascendants in the below while loop
        print('more checkpoints')
        parents_lca = False
        next_gen = True
        gen = 0
        gen_people = 2 ** gen
        gen_width_unit = max_widths[i] / (gen_people * 2)
        print(f'max_width is {max_widths[i]}')
        print(f'x before reassignment is {x}')
        # person2 will be positioned relative to person1. Initial_separation ensures that both halves stay separate.
        x = initial_width + gen_width_unit  # position of person1, person2
        initial_width = max_widths[i] + initial_separation * 2
        print(f'gen_width_unit={gen_width_unit} for {people[i].ref}')
        print(f'x={x}')
        y = - gen_diffs[i]
        node_name = human.name + '_' + str(human.ID)
        color = '#e5edc4'
        new_node = {'node_name': node_name, 'pos': {'x': x, 'y': y}, 'color': color, 'human': human}
        new_nodes = [new_node]
        all_nodes.append(new_node)
        unknownID = 0
        # this loop goes through each generation and makes a node (i.e., a dictionary for every human). Also, there is
        # a list that holds all the edges, or connections between nodes.
        reached_lca = False
        while next_gen:
            if reached_lca:
                break
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
                y = node['pos']['y'] + 1
                if node['human'] is not None:
                    try:
                        if node['human'].father not in lca and node['human'].mother not in lca:
                            x = node['pos']['x']  # position of connector is above node
                        else:
                            x = middle  # position of connector if one of parents is in lca.
                            parents_lca = True
                    except AttributeError:
                        x = node['pos']['x']
                else:
                    x = node['pos']['x']  # position of connector is above human.

                connector_node = {'node_name': node_name, 'style': style, 'label': label, 'height': height,
                                  'width': width, 'shape': shape, 'pos': {'x': x, 'y': y}}
                connector_nodes.append(connector_node)
                if not parents_lca:
                    edges.append(f"{connector_node['node_name']} -- {node['node_name']}")
                else:
                    extra_node = {'node_name': f'{node_name}_extra', 'style': style, 'label': label, 'height': height,
                                  'width': width, 'shape': shape, 'pos': {'x':x, 'y': y - 1}}
                    connector_nodes.append(extra_node)
                    edges.append(f"{extra_node['node_name']} -- {node['node_name']}")
                    edges.append(f"{connector_node['node_name']} -- {extra_node['node_name']}")
                if node['human'] is not None and node['human']:
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
                        gen_width_unit = max_widths[i] / (gen_people * 2)
                        direction = left_right[j]
                        if parent in lca:
                            x = middle + gen_width_unit * direction
                            reached_lca = True
                        else:
                            if parent in to_lca_people[i]:  # common ancestor must always be in the middle.
                                direction = left_right[i]
                            elif parent in flipping_parents[i]:
                                direction = left_right[i] * (-1)  # opposite direction of parent in common ancestor line
                            x = node['pos']['x'] + gen_width_unit * direction
                        try:  # add node name and color of node
                            node_name = parent.name + '_' + str(parent.ID)
                            color = colors[j]
                            node_human = parent
                        except AttributeError:  # if parent unknown, add a special node to tree.
                            unknownID += 1
                            node_name = 'Unknown' + '_' + str(gen) + '_' + str(j) + '_' + str(unknownID)
                            color = colors[2]
                            node_human = None
                        new_node = {'node_name': node_name, 'pos': {'x': x, 'y': y}, 'color': color,
                                    'human': node_human}
                        next_new_nodes.append(new_node)
                        # connect the new node with the connector node of son
                        edges.append(f"{new_node['node_name']} -- {connector_node['node_name']}")

            new_nodes = next_new_nodes
            for node in new_nodes:
                all_nodes.append(node)
    print('checkpoint5')
    to_dot_file = '''
    graph dotSrc {
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

    for i, line in enumerate(flipping_parents):
        for j, human in enumerate(line):
            try:
                print(f'flipping parent is {human.ref}')
                print(f'line parent is {to_lca_people[i][j].ref}')
            except AttributeError:
                print(None)
