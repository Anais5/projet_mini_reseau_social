def liste_tags(tags):
    liste = tags.split(",")
    if liste == [''] :
        liste.append('Sans_tag')
        print(liste)
        return liste
    else:
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
    html = '<body style="background-color:#ddd"/>'
    html += "<form method='post'><h1>Rechercher un article à propos de:</h1><br/>\n"
    for i in range(len(tags)):
        html += "<input type='checkbox' name='tag' value={}/> {}\n".format(tags[i], tags[i])
        if (i+1) % 5 == 0:
            html += "<br/>"
    html += "<br/><input type='submit' value='Rechercher'/></form>"
    return html

def separer_tags(tags):
    return tags.split("&")