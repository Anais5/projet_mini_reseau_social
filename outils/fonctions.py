def liste_tags(tags):
    liste = tags.split(",")
    for k in range(len(liste)):
        courant = liste[k]
        while courant[0] == " ":
            liste[k] = courant[1:]
            courant = liste[k]
        while courant[-1] == " ":
            liste[k] = courant[:-1]
            courant = liste[k]
    return liste