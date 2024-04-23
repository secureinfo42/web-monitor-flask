import matplotlib.pyplot as plt
from base64 import b64encode
import tempfile
import os

def get_graph(int_timing,int_size):

  # Données de démonstration: Temps de réponse en millisecondes pour différents services
  response_times = [int(int_timing), int(int_size)]
  services = ['Temps de réponse', 'Taille de la réponse']

  # Création du graphique à secteurs
  fig, ax = plt.subplots()
  wedges, texts, autotexts = ax.pie(response_times, labels=services, autopct='%1.1f%%', startangle=90, counterclock=False)

  # Conversion en graphique donut
  centre_circle = plt.Circle((0,0),0.70,fc='white')
  fig.gca().add_artist(centre_circle)

  # Ajout de légendes et de titres
  ax.set_title('Temps de réponse par service')
  plt.setp(autotexts, size=8, weight="bold")

  # Affichage du graphique
  # plt.savefig('/tmp/matplotlib.png')
  outfile = tempfile.mktemp()
  plt.savefig(outfile, bbox_inches='tight', dpi=300)

  png = open(outfile,'rb').read()
  os.unlink(outfile)

  return( b64encode(png).decode() )

