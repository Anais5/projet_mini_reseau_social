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

def page_recherche_tags(tags):
    html = "<h1>Rechercher un article à propos de:</h1><br/>\n"
    for i in range(len(tags)):
        html += "<input type='checkbox'/> {}\n".format(tags[i])
        if (i+1) % 5 == 0:
            html += "<br/>"
    html += "<br/><input type='button' value='recherhcer'/>"
    return html