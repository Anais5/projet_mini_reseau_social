# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).
import socket, sys, threading

class ThreadReception(threading.Thread):
    """Objet thread gérant la réception des messages."""

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion
        self.__is_killed = False
        self.messages = []

    def run(self):
        while self.__is_killed == False:
            message_recu = self.connexion.recv(1024)
            message_recu = message_recu.decode('utf-8')
            self.messages.append(message_recu)
            print("*" + message_recu + "*")
            '''if message_recu == '' or message_recu.upper() == "FIN":
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
        th_E.kill()
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()'''

    def get_messages(self):
        return self.messages

    def clear_all(self):
        self.messages = []

    def clear_message(self, m):
        self.messages.remove(m)

    def kill(self):
        self.__is_killed = True

class ThreadEmission(threading.Thread):
    """Objet thread gérant l'émission des messages."""

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion
        self.__is_killed = False
        self.messages = []

    def run(self):
        while self.__is_killed == False:
            message_emis = input()
            self.messages.append(message_emis)
            message_emis = message_emis.encode('utf-8')
            '''if message_emis.upper() == "FIN":
                self.kill()'''

            self.connexion.send(message_emis)
        '''
        th_R.kill()
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()'''

    def get_messages(self):
        return self.messages

    def clear_all(self):
        self.messages = []

    def clear_message(self, m):
        self.messages.remove(m)

    def kill(self):
        self.__is_killed = True


def run_client(port):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    # Programme principal - Établissement de la connexion :
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        connexion.connect((host, port))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")


    # Dialogue avec le serveur : on lance deux threads pour gérer
    # indépendamment l'émission et la réception des messages :
    th_E = ThreadEmission(connexion)
    th_R = ThreadReception(connexion)
    th_E.start()
    th_R.start()

    while 1:
        for m in th_E.get_messages():
            if m.upper() != "FIN":
                th_E.clear_message(m)
            else:

                th_R.clear_all()
                th_E.clear_all()
                th_E.kill()
                th_R.kill()
                print("FIN")
                return

        for m in th_R.get_messages():
            print(f"A mettre dans la base de données : {m}")
            th_R.clear_message(m)

# Définition d'un serveur réseau gérant un système de CHAT simplifié.
class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.clients_co = {}

    def run(self):
        # Dialogue avec le client :
        nom = self.getName()  # Chaque thread possède un nom
        while 1:
            msgClient = self.connexion.recv(1024)
            msgClient = msgClient.decode('utf-8')
            if msgClient.upper() == "FIN" or msgClient == "":
                break
            message = "%s> %s" % (nom, msgClient)
            print(message)
            # Faire suivre le message à tous les autres clients :
            for cle in self.clients_co:
                if cle == nom:  # ne pas le renvoyer à l'émetteur
                    continue
                msg = message.encode('utf-8')
                client = self.clients_co[cle]
                client.send(msg)

        # Fermeture de la connexion :
        self.connexion.close()  # couper la connexion côté serveur
        del self.clients_co[nom]  # supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % nom)

        # Le thread se termine ici

def run_serveur(port):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    # Initialisation du serveur - Mise en place du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.bind((host, port))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()
    print("Serveur prêt, en attente de requêtes ...")
    mySocket.listen(5)

    # Attente et prise en charge des connexions demandées par les clients :

    while 1:
        connexion, adresse = mySocket.accept()
        # Créer un nouvel objet thread pour gérer la connexion :
        th = ThreadClient(connexion)
        th.start()
        # Mémoriser la connexion dans le dictionnaire :
        it = th.getName()  # identifiant du thread
        th.clients_co[it] = connexion
        print("Client %s connecté, adresse IP %s, port %s." % (it, adresse[0], adresse[1]))

        # Dialogue avec le client :
        connexion.send("Vous êtes connecté. Envoyez vos messages.".encode('utf-8'))