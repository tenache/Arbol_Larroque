from arbol_tryout import Person, tree
import importlib
import arbol2

importlib.reload(arbol2)
from graph_tree import to_graphic_tree

print('hello')
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
Gerardo.assign_mother(Palma)
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
to_graphic_tree(Enzo, Laura)
