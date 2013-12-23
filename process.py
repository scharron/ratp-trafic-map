from xlrd import open_workbook
import re

stations = {}

import unidecode
def clean(name):
  orig = str(name)
  name = unidecode.unidecode(name.upper())
  name = name.replace("4", "QUATRE")
  name = re.sub("[^A-Z]", " ", name)
  name = name.replace("ASNIERES", "")
  name = name.replace("GENNEVILLIERS", "")
  name = name.replace("AUBERVILLIERS", "")
  name = name.replace("PANTIN", "")
  name = name.replace("HOPITAL SAINT LOUIS", "")
  name = name.replace("GRANDE ARCHE", "")
  name = name.replace("LEON BLUM", "")
  name = name.replace("HOPITAL PAUL BROUSSE", "")
  name = name.replace("ADOLPHE CHERIOUX", "")
  name = name.replace("LE MARAIS", "")
  name = name.replace("TOURELLE", "")
  name = name.replace("AVENUE GEORGES MANDEL", "")
  name = name.replace("GENERAL LECLERC", "")
  name = name.replace("MARECHAL DE LATTRE DE TASSIGNY", "")
  name = name.replace("CITE DES ARTS", "")
  name = name.replace("JARDIN DES PLANTES", "")
  name = name.replace("VERDUN", "")
  name = name.replace("GRENELLE", "")
  name = name.replace("JACQUES DUCLOS", "")
  name = name.replace("PARC DE BAGNOLET", "")
  name = name.replace("RIVOLI", "")
  name = name.replace("MUSEE DU LOUVRE", "")
  name = name.replace("FRANKLIN D", "FRANKLIN")
  name = name.replace("HOPITAL HENRI MONDOR", "")
  name = name.replace("ET MARIE", "")
  name = name.replace("RUE", "")
  name = name.replace("FELIX EBOUE", "")
  name = name.replace("CRETEIL", "")
  name = name.replace("PLACE DE", "PLACE")
  name = name.replace("BIBLIOTHEQUE FRANCOIS MITTERRAND", "BIBLIOTHEQUE")
  name = name.replace("JARDIN D ACCLIMATATION", "")
  name = name.replace("GARE BASSE", "")
  name = name.replace("GARE HAUTE", "")
  name = name.replace("PREFECTURE  HOTEL DE VILLE", "PREFECTURE")
  name = name.replace("  ", " ")
  name = name.replace("  ", " ")
  name = re.sub("^ *", "", name)
  name = re.sub(" *$", "", name)
  if len(name) == 0:
    print("!!!", orig)
  return name

def int_or_string(t):
  try:
    return int(t)
  except:
    pass
  return str(t)

for year in ("2011", "2012"):
  wb = open_workbook("%s_trafic_annuel.xls" % year)
  sheet = wb.sheets()[0]
  for row in range(sheet.nrows):
    if sheet.cell(row, 2).value != "Métro":
      continue
    name = clean(sheet.cell(row, 3).value)
    if len(name) == 0:
      continue
    trafic = sheet.cell(row, 4).value
    rank = sheet.cell(row, 1).value
    lines = [sheet.cell(row, i).value for i in range(5, 10)]
    stations[name] = {"trafic": trafic, "lines": [int_or_string(l) for l in lines if l != 0 and len(str(l)) > 0 and str(l)[0].isdigit()], "rank": rank}

  import csv
  reader = csv.reader(open("ratp_arret_graphique.csv", newline=""), delimiter='#')

  #print(list(stations.keys()))
  for row in reader:
    if row[5] not in ["metro"]:
      continue
    name = clean(row[3])
    if name not in stations:
      print(row)
      print(row[3], name)
      continue
    stations[name]["latitude"] = float(row[1])
    stations[name]["longitude"] = float(row[2])
    stations[name]["name"] = row[3]
    stations[name]["key"] = name

  #print([s for s, d in stations.items() if "name" not in d])

  import json

  def dist(d1, d2):
    x = d1["latitude"] - d2["latitude"]
    y = d1["longitude"] - d2["longitude"]
    return x * x + y * y

  parts = {}
  for key, detail in stations.items():
    stations[key]["connexion"] = {}
    for line in detail["lines"]:
      if line not in parts:
        parts[line] = []

      same_line = [(s, d) for s, d in stations.items() if line in d["lines"]]
      same_line.sort(key=lambda e: dist(detail, e[1]))

      nb = 2
      if key in ["MAISON BLANCHE", "BOULOGNE JEAN JAURES", "JAVEL ANDRE CITROEN", "LA FOURCHE", "BOTZARIS"]:
        nb = 3

      # TERMINUS
      if line == 1 and key in ["CHATEAU DE VINCENNES", "LA DEFENSE"]:
        nb = 1
      if line == 2 and key in ["NATION", "PORTE DAUPHINE"]:
        nb = 1
      if line == 3 and key in ["GALLIENI", "PONT DE LEVALLOIS BECON"]:
        nb = 1
      if line == "3bis" and key in ["GAMBETTA", "PORTE DES LILAS"]:
        nb = 1
      if line == 4 and key in ["PORTE D ORLEANS", "PORTE DE CLIGNANCOURT"]:
        nb = 1
      if line == 5 and key in ["PLACE D ITALIE", "BOBIGNY PABLO PICASSO"]:
        nb = 1
      if line == 6 and key in ["NATION", "CHARLES DE GAULLE ETOILE"]:
        nb = 1
      if line == 7 and key in ["VILLEJUIF LOUIS ARAGON", "MAIRIE D IVRY", "LA COURNEUVE MAI QUATRE"]:
        nb = 1
      if line == "7bis" and key in ["LOUIS BLANC"]:
        nb = 1
      if line == 8 and key in ["POINTE DU LAC", "BALARD"]:
        nb = 1
      if line == 9 and key in ["MAIRIE DE MONTREUIL", "PONT DE SEVRES"]:
        nb = 1
      if line == 10 and key in ["BOULOGNE PONT DE SAINT CLOUD", "GARE D AUSTERLITZ"]:
        nb = 1
      if line == 11 and key in ["CHATELET", "MAIRIE DES LILAS"]:
        nb = 1
      if line == 12 and key in ["PORTE DE LA CHAPELLE", "MAIRIE D ISSY"]:
        nb = 1
      if line == 13 and key in ["SAINT DENIS UNIVERSITE", "LES COURTILLES", "CHATILLON MONTROUGE"]:
        nb = 1
      if line == 14 and key in ["SAINT LAZARE", "OLYMPIADES"]:
        nb = 1

      best = [s for (s,d) in same_line[1:(nb + 1)]]
      for b in best:
        parts[line].append((key, b))
      #stations[key]["connexion"][line] = best

  lines = []
  for line, parts in parts.items():
    links = {}
    for part in parts:
      if part[0] not in links:
        links[part[0]] = set()
      if part[1] not in links:
        links[part[1]] = set()
      links[part[0]].add(part[1])
      links[part[1]].add(part[0])

    ends = [e for e in links.keys() if len(links[e]) == 1]
    seen = set()

    for (l, a, b) in [(2, "STALINGRAD", "COLONEL FABIEN"),
                      (2, "ANVERS", "FUNICULAIRE"),
                      (2, "COURCELLES", "CHARLES DE GAULLE ETOILE"),
                      (3, "EUROPE", "HAVRE CAUMARTIN"),
                      (3, "ARTS ET METIERS", "REPUBLIQUE"),
                      (3, "TEMPLE", "PERE LACHAISE"),
                      (4, "VAVIN", "SAINT PLACIDE"),
                      (5, "BOBIGNY RAYMOND QUENEAU", "HOCHE"),
                      (5, "GARE DE L EST", "STALINGRAD"),
                      (7, "STALINGRAD", "CHATEAU LANDON"),
                      (7, "LE KREMLIN BICETRE", "PORTE D ITALIE"),
                      (7, "PORTE D IVRY", "PORTE D ITALIE"),
                      (7, "PORTE DE CHOISY", "MAISON BLANCHE"),
                      (7, "LES GOBELINS", "PLACE MONGE"),
                      (7, "CHAUSSEE D ANTIN LA FAYETTE", "PYRAMIDES"),
                      (7, "QUATRE CHEMINS", "CORENTIN CARIOU"),
                      (7, "PONT MARIE", "JUSSIEU"),
                      (7, "JUSSIEU", "PONT MARIE"),
                      (8, "REPUBLIQUE", "SAINT SEBASTIEN FROISSART"),
                      (8, "LIBERTE", "PORTE DOREE"),
                      (8, "MICHEL BIZOT", "PORTE DE CHARENTON"),
                      (8, "MONTGALLET", "FAIDHERBE CHALIGNY"),
                      (8, "CONCORDE", "OPERA"),
                      (9, "HAVRE CAUMARTIN", "SAINT LAZARE"),
                      (9, "PORTE DE MONTREUIL", "BUZENVAL"),
                      (9, "MIROMESNIL", "FRANKLIN ROOSEVELT"),
                      (9, "PORTE DE SAINT CLOUD", "MICHEL ANGE MOLITOR"),
                      (10, "MAUBERT MUTUALITE", "JUSSIEU"),
                      (10, "MIRABEAU", "EGLISE D AUTEUIL"),
                      (10, "EGLISE D AUTEUIL", "CHARDON LAGACHE"),
                      (10, "JAVEL ANDRE CITROEN", "EGLISE D AUTEUIL"),
                      (10, "CHARDON LAGACHE", "MICHEL ANGE AUTEUIL"),
                      (10, "PORTE D AUTEUIL", "MICHEL ANGE MOLITOR"),
                      (12, "TRINITE D ESTIENNE D ORVES", "SAINT GEORGES"),
                      (12, "FRONT POPULAIRE", "MARX DORMOY"),
                      (13, "PLACE CLICHY", "SAINT LAZARE"),
                      (13, "SAINT DENIS UNIVERSITE", "SAINT DENIS PORTE DE PARIS"),
                      (14, "BIBLIOTHEQUE", "BERCY"),
                      (14, "BIBLIOTHEQUE", "GARE DE LYON"),
                      (14, "PYRAMIDES", "SAINT LAZARE"),
                      ("7bis", "DANUBE", "PLACES FETES"),
                      ]:
      if l != line:
        continue
      if a in links and b in links[a]:
        links[a].remove(b)
      if b in links and a in links[b]:
        links[b].remove(a)

    for (l, a, b) in [(3, "REPUBLIQUE", "PARMENTIER"),
                      (5, "STALINGRAD", "GARE DU NORD"),
                      (7, "LE KREMLIN BICETRE", "MAISON BLANCHE"),
                      (7, "LES GOBELINS", "CENSIER DAUBENTON"),
                      (7, "PYRAMIDES", "OPERA"),
                      (8, "LIBERTE", "PORTE DE CHARENTON"),
                      (9, "HAVRE CAUMARTIN", "SAINT AUGUSTIN"),
                      (10, "MIRABEAU", "CHARDON LAGACHE"),
                      (14, "GARE DE LYON", "CHATELET"),
                  ]:
      if l != line:
        continue
      if a not in links:
        links[a] = set()
      if b not in links:
        links[b] = set()
      links[a].add(b)
      links[b].add(a)

    paths = []
    for end in ends:
      current = str(end)
      path = [current]
      while True:
        for other in links[current]:
          link = (min(current, other), max(current, other))
          if link not in seen:
            seen.add(link)
            path.append(other)
            current = other
            break
        else:
          break
      paths.append(path)
    if line == 10:
      paths.append(["JAVEL ANDRE CITROEN", "EGLISE D AUTEUIL", "MICHEL ANGE AUTEUIL", "PORTE D AUTEUIL", "BOULOGNE JEAN JAURES"])
    lines.append({"key": line, "paths": [p for p in paths if len(p) > 1]})

  all_data = {"freq": stations,
              "lines": lines}
  open("ratp.%s.json" % year, "w").write(json.dumps(all_data, indent=2))
