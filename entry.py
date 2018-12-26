class Entry:
    def __init__(self, title, issuer, secret, algo, digits, type):
        self.id = -1
        self.title = title
        self.issuer = issuer
        self.secret = secret
        self.algo = algo
        self.digits = digits
        self.type = type

    def __repr__(self):
        return str(self.id) + ": " + self.issuer + "\t" + self.title

    def __str__(self):
        return str(self.id) + ": " + self.issuer + "\t" + self.title

    def setID(self, id):
        self.id = id

    def getTitle(self):
        return self.title

    def getUser(self):
        return self.user

    def getSecret(self):
        return self.secret

    def getType(self):
        return self.type

    def getID(self):
        return self.id

    def getFileEntry(self):
        return self.title + ";" + self.issuer + ";" + self.secret + ";" + self.algo + ";" + self.digits + ";" + self.type
