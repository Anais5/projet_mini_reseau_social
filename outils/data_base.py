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

    def recuperer_compte(self, login, mdp):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            curs = c.execute("""SELECT login, mdp FROM membres WHERE (login = ? and mdp = ?)""",
                             (login, mdp)
            )
            c.commit()
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
        id = curs.fetchone()[0]
        return id

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
            WHERE auteur_id = ?, titre = ?, contenu = ?
            ORDER BY id""",
                            (auteur_id, titre, contenu)
            )
        id = curs.fetchall()[-1]
        return id

    def inserer_tag(self, id, tag):
        self.conn = sql.connect(self.dir)
        with self.conn as c:
            c.execute("""INSERT INTO tags
            VALUES (?, ?)""",
                    (id, tag)
                )
        c.commmit