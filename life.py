#!/usr/bin/python
import sys
#from LifeManager import LifeManager
from RandomLifeManager import RandomLifeManager
from LifeApplication import LifeApplication

# Create Life
#born_if = (1, ); alive_if = (1, );  # Gnarl

#born_if = (3, ); alive_if = (4, 5, 6, 7, 8);  # Coral
#born_if = (1, 3, 5, 7); alive_if = (1, 3, 5, 7);  # Replicator
#born_if = (2, ); alive_if = ();  # Seeds
#born_if = (2, 3, 4); alive_if = ();  # Serviettes
#born_if = (3, ); alive_if = (0, 1, 2, 3, 4, 5, 6, 7, 8);  # Life without Death
#born_if = (3, 4, 5); alive_if = (4, 5, 6, 7);  # Assimilation
#born_if = (3, 4, 5); alive_if = (5, );  # Long Life
#born_if = (3, 5, 6, 7, 8); alive_if = (5, 6, 7, 8);  # Diamoeba
#born_if = (3, 6); alive_if = (1, 2, 5);  # 2x2
#born_if = (3, 6, 7, 8); alive_if = (2, 3, 5, 6, 7, 8);  # Stains
#born_if = (4, 5, 6, 7, 8); alive_if = (2, 3, 4, 5);  # Walled Cities

#born_if = (3, 7, 8); alive_if = (2, 3, 5, 6, 7, 8);  # Coagulations
#born_if = (3, 6, 8); alive_if = (2, 4, 5);  # Move
#born_if = (3, 6, 7, 8); alive_if = (3, 4, 6, 7, 8);  # Day & Night
#born_if = (3, 5, 7); alive_if = (1, 3, 5, 8);  # Amoeba
#born_if = (3, 5, 7); alive_if = (2, 3, 8);  # Pseudo Life
#born_if = (3, 4); alive_if = (3, 4);  # 34 Life
#born_if = (3, 6); alive_if = (2, 3);  # HighLife
#born_if = (3, ); alive_if = (1, 2, 3, 4, 5);  # Maze
born_if = (3, ); alive_if = (2, 3);  # Classic Life

life = RandomLifeManager(100, 100, born_if, alive_if)

# Create Qt application and main widget
app = LifeApplication(life)

sys.exit(app.exec_())
