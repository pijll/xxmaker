import unittest

import Game
import Company


class TestCompany(unittest.TestCase):
    def test_standard_company(self):
        # Arrannge

        # Act
        company = Company.Company("Some Railroad")

        # Assert
        self.assertEqual("Some Railroad", company.name, "Name")
        self.assertEqual(10, company.num_shares, "Number of shares")

    def test_add_to_game(self):
        # Arrange
        game = Game.Game("1801")
        company = Company.Company("Some Railroad")

        # Act
        game.add_company(company)

        # Assert
        self.assertEqual(1, len(game.companies), "Number of companies")
        self.assertEqual("Some Railroad", game.companies[0].name)

