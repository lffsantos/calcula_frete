import unittest
from axado import Transporte, ler_arquivo

__author__ = 'lucas'


class TestTransporte(unittest.TestCase):

    def setUp(self):
        self.tabela = {"tabela1": {}, "tabela2": {}}
        self.tabela["tabela1"]["preco_p_kg"] = ler_arquivo("teste_por_kg.csv")
        self.tabela["tabela1"]["rota"] = ler_arquivo("teste.csv")
        self.tabela["tabela2"]["rota"] = ler_arquivo("teste2.tsv")
        self.tabela["tabela2"]["preco_p_kg"] = ler_arquivo("teste_por_kg.csv")
        self.transporte = Transporte("florianopolis","brasilia", 50, 7, self.tabela)

    def test_ler_arquivo(self):
        teste = [{'kg': 'flo', 'prazo': '3', 'seguro': '3', 'destino': 'brasilia', 'origem': 'florianopolis', 'fixa': '13'},
                 {'kg': 'flo', 'prazo': '3', 'seguro': '3', 'destino': 'curitiba', 'origem': 'florianopolis', 'fixa': '7'},
                 {'kg': 'central', 'prazo': '1', 'seguro': '3', 'destino': 'florianopolis', 'origem': 'saopaulo', 'fixa': '8'}]
        self.assertEqual(self.tabela["tabela1"]["rota"], teste)

    def test_calcula_seguro(self):
        seguro = self.transporte.valor_seguro(4)
        self.assertEqual(2.0, seguro)

        self.transporte.nota_fiscal = 30
        seguro = self.transporte.valor_seguro(4)
        self.assertEqual(1.2, seguro)

    def test_get_rota(self):
        rota = self.transporte.get_rota(self.tabela["tabela1"])
        self.assertEqual(rota, {'kg': 'flo', 'prazo': '3', 'seguro': '3', 'destino': 'brasilia', 'origem': 'florianopolis', 'fixa': '13'})
        self.transporte = Transporte("florianopolis","salvador", 50, 7, self.tabela["tabela1"])
        rota = self.transporte.get_rota(self.tabela["tabela1"])
        self.assertEqual({}, rota)

    def test_calcula_valor_frete(self):
        rota = self.transporte.get_rota(self.tabela["tabela1"])
        valor = self.transporte.calcula_valor_frete(rota, self.tabela["tabela1"])
        self.assertEqual("104.79", valor)

        self.transporte = Transporte("saopaulo","florianopolis", 50, 130, self.tabela["tabela1"])

        rota = self.transporte.get_rota(self.tabela["tabela1"])
        valor = self.transporte.calcula_valor_frete(rota, self.tabela["tabela1"])
        self.assertEqual("1393.09", valor)

    def test_valor_faixa(self):
        valor = self.transporte.valor_faixa("flo", self.tabela["tabela1"]["preco_p_kg"])
        self.assertEqual(84, valor)
        self.transporte.peso = 30
        valor = self.transporte.valor_faixa("central", self.tabela["tabela1"]["preco_p_kg"])
        self.assertEqual(300, valor)

    def test_prazo(self):
        rota = self.transporte.get_rota(self.tabela["tabela1"])
        self.assertEqual('3', self.transporte.get_prazo(rota))
        self.transporte = Transporte("saopaulo","florianopolis", 50, 130, self.tabela)
        rota = self.transporte.get_rota(self.tabela["tabela1"])
        self.assertEqual('1', self.transporte.get_prazo(rota))

    def test_frete(self):

        self.assertEqual(self.transporte.frete().sort(), [('tabela2', '2', '90.43'), ('tabela1', '3', '104.79')].sort())

        self.transporte = Transporte("saopaulo","florianopolis", 50, 130, self.tabela)

        self.assertEqual(self.transporte.frete().sort(), [('tabela1', '1', '1393.09')].sort())

        self.transporte = Transporte("florianopolis","curitiba",50,100, self.tabela)

        self.assertEqual(self.transporte.frete().sort(), [('tabela2', '-', '-'), ('tabela1', '3', '540.96')].sort())

if __name__ == '__main__':
    unittest.main()