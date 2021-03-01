import sqlite3 as sql

class DataBase:
    def __init__(self, data_base_name, data_base_dir):
        self.name = data_base_name
        self.dir = data_base_dir
        self.conn = sql.connect(data_base_dir)

    def recuperer_articles(self):  # renvoie une liste de tuples
        # de la forme (login, cree_le, titre, contenu)
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
        with self.conn as c:
            curs = c.execute(
                """INSERT INTO articles (auteur_id, titre, contenu)
                    VALUES (?, ?, ?)""",
                (auteur_id, titre, contenu)
            )
            c.commit()  # ne pas oublier de «valider» lorsqu'une table est modifiée.

    def supprimer_article(self, id_article):
        with self.conn as c:
            curs = c.execute(
                """DELETE FROM articles WHERE id = ?""",
                (id_article,)
            )
            c.commit()