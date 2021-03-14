import sqlite3 as sql


class DataBase:
    def __init__(self, data_base_dir):
        self.dir = data_base_dir
        self.conn = sql.connect(data_base_dir)

    def recuperer_articles(self):  # renvoie une liste de tuples
        # de la forme (login, cree_le, titre, contenu)
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute(
                """SELECT articles.id AS id_article, login, cree_le, titre, contenu
                    FROM membres JOIN articles
                    ON membres.id = articles.auteur_id
                    ORDER BY articles.cree_le DESC
                """
            )
            return curs.fetchall()

    def inserer_article(self, auteur_id, titre, contenu):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            c.execute("""INSERT INTO articles (auteur_id, titre, contenu) VALUES (?, ?, ?)""",
                (auteur_id, titre, contenu)
            )
            c.commit()  # ne pas oublier de «valider» lorsqu'une table est modifiée.

    def supprimer_article(self, id_article):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            c.execute("""DELETE FROM articles WHERE id = ?""",
                    (id_article,)
            )
            c.commit()

    def supprimer_compte(self, auteur_id, login):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            c.execute("""DELETE FROM articles WHERE auteur_id = ?""",
                      (auteur_id,)
            )
            c.execute("""DELETE FROM membres WHERE login = ?""",
                      (login,)
            )
            c.commit()


    def recuperer_compte(self, login):
        self.conn = sql.connect(self.dir)
        curs = self.conn.cursor()
        curs.execute("""SELECT login, mdp FROM membres WHERE login = ?""",
                     (login,)
                     )
        return curs.fetchall()

    def recuperer_mdp(self, login):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT mdp FROM membres WHERE login = ?""",
                     (login,)
            )
        return curs.fetchone()

    def verif_pseudo(self, login):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT login FROM membres WHERE (login = ?)""",
                             (login,)
            )
        return curs.fetchone()

    def get_membre_id(self, login):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT id FROM membres WHERE (login = ?)""",
                             (login,)
            )
        id = curs.fetchone()
        if id:
            return id[0]
        return id

    def recuperer_articles_membre(self, id):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT id AS id_article, cree_le, titre, contenu
                                FROM articles
                                WHERE (auteur_id = ?)
                                ORDER BY articles.cree_le DESC""",
                             (id,)
            )
        return curs.fetchall()

    def ajouter_membre(self, login, mdp):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            c.execute("""INSERT INTO membres (login, mdp) VALUES (?, ?)""",
                              (login, mdp)
            )
            c.commit()

    def recuperer_id(self, auteur_id, titre, contenu):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT id FROM articles
            WHERE auteur_id = ? AND titre = ? AND contenu = ?
            ORDER BY id""",
                            (auteur_id, titre, contenu)
            )
        id_a = curs.fetchall()[-1]
        return id_a


    def inserer_tag(self, id, tag):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            c.execute("""INSERT INTO tags
            VALUES (?, ?)""",
                    (str(tag), id[0])
                )
            c.commit()

    def rechercher_tags(self):
        tags = []
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT DISTINCT tag
            FROM tags""")
            for element in curs:
                tags.append(element[0])
        return tags

    def recuperer_id_article(self, tag):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT id 
            FROM tags WHERE tags.tag = ?""", 
            (tag,))
            articles = curs.fetchall()
        return articles

    def recuperer_mdp(self, login):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT mdp FROM membres WHERE login = ?""",
                     (login,)
            )
        return curs.fetchone()