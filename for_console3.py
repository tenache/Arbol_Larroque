import importlib
import arbol3
importlib.reload(arbol3)
from arbol3 import load_csv_tree
a = load_csv_tree('Arbol_Genealogico.csv')