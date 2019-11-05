#from Output import mm


class Game:
    def __init__(self, name, author, currency=''):
        self.name = name
        self.companies = {}
        self.trains = []
        self.privates = []
        self.tiles = []
        self.maps = []
        self.stockmarket = None
        self.author = author
        self.currency = currency
#        self.tilesize = 38*mm   # side to side

    def add_company(self, company):
        self.companies[company.abbreviation] = company
        company.game = self

    def add_train(self, number, train):
        self.trains.append((number, train))
        train.game = self

    def add_private(self, private):
        self.privates.append(private)
        private.game = self

    def add_tile(self, tile):
        self.tiles.append(tile)
        tile.game = self

    def add_map(self, map):
        self.maps.append(map)
        map.game = self

    def add_stockmarket(self, stockmarket):
        self.stockmarket = stockmarket
