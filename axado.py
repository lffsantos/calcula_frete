# -*- coding: utf-8 -*-
import sys
import csv
__author__ = 'lucas'


class Transporte:

    def __init__(self, origem,destino,nota_fiscal,peso):
        self.tabela = {"tabela1": {}, "tabela2": {}}
        self.tabela["tabela1"]["rota"] = self.ler_arquivo("tabela/rotas.csv")
        self.tabela["tabela1"]["preco_p_kg"] = self.ler_arquivo("tabela/preco_por_kg.csv")
        self.tabela["tabela2"]["rota"] = self.ler_arquivo("tabela2/rotas.tsv")
        self.tabela["tabela2"]["preco_p_kg"] = self.ler_arquivo("tabela2/preco_por_kg.tsv")
        self.origem = origem
        self.destino = destino
        self.nota_fiscal = int(nota_fiscal)
        self.peso = int(peso)

    def valor_seguro(self, seguro):
        return (self.nota_fiscal * seguro) / float(100)

    def valor_faixa(self, faixa, tabela):
        for t in tabela:
            if t["nome"] == faixa:
                try:
                    if float(t["inicial"]) <= self.peso and float(t["final"]) > self.peso:
                        return float(t["preco"]) * self.peso
                except ValueError:
                    return float(t["preco"]) * self.peso

    def calcula_frete(self, rota, tabela):
        subtotal = 0
        subtotal += self.valor_seguro(int(rota['seguro']))
        if rota.get("fixa"):
            subtotal += int(rota['fixa'])
        subtotal += self.valor_faixa(rota["kg"], self.tabela[tabela]["preco_p_kg"])
        if rota.get("alfandega"):
            subtotal += subtotal * (int(rota["alfandega"])/float(100))
        icms = rota.get("icms", 6)
        total = subtotal / ((100 - int(icms))/float(100))

        return ("%.2f" % total)

    def get_prazo(self, rota):
        return rota['prazo']

    def ler_arquivo(self, file):
        '''
          Entre com o arquivo, as chaves do dicionário sera os valores do header
          :return: lista de dict com os dados da do arquivo
        '''
        if ".tsv" in file:
            delimiter = "\t"
        else:
            delimiter = ","
        cr = csv.reader(open(file,"rb"), delimiter=delimiter)
        header = next(cr,None)
        dados = []
        for row in cr:
            arquivo = {}
            for i in xrange(0, len(header)):
                arquivo[header[i]] = row[i]
            dados.append(arquivo)

        return dados

    def processa_calculos(self):
        output = []
        for t in self.tabela:
            rota = self.get_rota(self.origem,self.destino, self.tabela[t])
            if rota:
                if rota.get("excedeu_limite"):
                    print(t, "-","-")
                else:
                    print(t, self.get_prazo(rota), self.calcula_frete(rota, t))
            else:
                print("rota nao encontrada!")

    def get_rota(self, origem, destino, tabela):
        dados_rota = {}
        for line in tabela['rota']:
            if origem in line['origem'] and destino in line['destino']:
                if line.get("limite", self.peso) <= self.peso:
                    dados_rota = line
                    break
                else:
                    dados_rota["excedeu_limite"] = True
        return dados_rota

if __name__ == '__main__':

    '''
     leitura dos parametros de entrada
    '''
    origem = "saopaulo"
    destino = "florianopolis"
    nota_fiscal = 50
    peso = 130
    # origem = sys.argv[1]
    # destino = sys.argv[2]
    # nota_fiscal = sys.argv[3]
    # peso = sys.argv[4]
    # print origem, destino, nota_fiscal, peso

    transporte = Transporte(origem,destino,nota_fiscal,peso)
    transporte.processa_calculos()
    # rota = transporte.get_rota(origem, destino, transporte.tabela["tabela1"]["rota"])
    # if not rota:
    #     print("Não temos essa rota")
    # else:
    #     # print(rota)
    #     # print(transporte.calcula_prazo(rota))
    #     transporte.formata_saida()


