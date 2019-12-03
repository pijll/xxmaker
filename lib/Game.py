class Game:
    def __init__(self, name, author, license_file, currency=''):
        self.name = name
        self.companies = {}
        self.trains = []
        self.privates = []
        self.tiles = []
        self.maps = []
        self.stockmarket = None
        self.author = author
        self.currency = currency
        self.papers = []
        self._tokens = []

        try:
            with open(license_file) as infile:
                license_txt = infile.read()
        except OSError:
            raise Exception(f"No license file found ('{license_file}')") from None
        self.license = license_txt

    def add_company(self, *companies):
        for company in companies:
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
        stockmarket.game = self

    def add_paper(self, *papers):
        self.papers += papers

    def add_token(self, token):
        self._tokens.append(token)

    @property
    def tokens(self):
        if self.stockmarket and self.stockmarket.has_par_box:
            tokens_per_company = 3      # stock vale; revenue chart; par value
        else:
            tokens_per_company = 2      # stock value; revenue chart

        tokens = []
        for company in self.companies.values():
            tokens += [company.logo] * (company.n_stations + tokens_per_company)
        return tokens + self._tokens
