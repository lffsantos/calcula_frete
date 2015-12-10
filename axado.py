# -*- coding: utf-8 -*-
import sys
import csv
__author__ = 'lucas'


def ler_arquivo(file):
    '''
      Entre com o arquivo, as chaves do dicionário sera os valores do header
      :return: lista de dict com os dados da do arquivo
    '''
    if ".tsv" in file:
        delimiter = "\t"
    else:
        delimiter = ","
    file = open(file,"r")
    cr = csv.reader(file, delimiter=delimiter)
    header = next(cr,None)
    dados = []
    for row in cr:
        arquivo = {}
        for i in range(0, len(header)):
            arquivo[header[i]] = row[i]
        dados.append(arquivo)
    file.close()
    return dados


class Transporte:

    def __init__(self, origem, destino, nota_fiscal, peso, tabelas):
        self.tabela = tabelas
        self.origem = origem
        self.destino = destino
        self.nota_fiscal = float(nota_fiscal)
        self.peso = float(peso)

    def valor_seguro(self, seguro):
        '''
        calculo do seguro
        '''
        return (self.nota_fiscal * seguro) / float(100)

    def valor_faixa(self, faixa, tabela_preco_p_kg):
        '''
        retorna o calculo do peso para uma faixa de peso
        exemplo: peso = 5, faixa = 'flo'
         nome,inicial,final,preco
         flo,0,10,12
         flo,11,20,11

         return peso*12
        '''

        for t in tabela_preco_p_kg:
            if t["nome"] == faixa:
                # Try/except adicionado pois as vezes o valor final pode ser "--" que da erro ao tentar converter para float então a faixa do peso será essa
                try:
                    if float(t["inicial"]) <= self.peso and float(t["final"]) > self.peso:
                        return float(t["preco"]) * self.peso
                except ValueError:
                    return float(t["preco"]) * self.peso

    def calcula_valor_frete(self, rota, tabela):
        subtotal = 0
        subtotal += self.valor_seguro(float(rota['seguro']))
        if rota.get("fixa"):
            subtotal += float(rota['fixa'])
        subtotal += self.valor_faixa(rota["kg"], tabela["preco_p_kg"])
        if rota.get("alfandega"):
            subtotal += subtotal * (float(rota["alfandega"])/float(100))
        icms = rota.get("icms", 6)
        total = subtotal / ((100 - float(icms))/float(100))

        return ("%.2f" % total)

    def get_prazo(self, rota):
        return rota['prazo']

    def frete(self):
        '''
        gerência o frete, pega a rota informada, calcula o frete e o prazo
        '''
        output = []
        for t in self.tabela:
            rota = self.get_rota(self.tabela[t])
            if rota:
                if rota.get("excedeu_limite"):
                    output.append((t, "-","-"))
                else:
                    output.append((t, self.get_prazo(rota), self.calcula_valor_frete(rota, self.tabela[t])))
            else:
                print("rota nao encontrada!")

        return output

    def format_output(self, frete):
        '''
        formata os dados de saída
        '''
        for f in frete:
            print("%s: %s, %s" % (f[0],f[1],f[2]))

    def get_rota(self, tabela):
        '''
        retorna a linha com a rota solicitada na tabela
        '''
        dados_rota = {}
        for line in tabela['rota']:
            if self.origem == line['origem'] and self.destino == line['destino']:
                limite =  float(line.get("limite", 0))
                if limite == 0 or limite >= self.peso:
                    dados_rota = line
                    break
                else:
                    dados_rota["excedeu_limite"] = True
        return dados_rota

if __name__ == '__main__':

    '''
     leitura dos parametros de entrada
    '''
    origem = sys.argv[1]
    destino = sys.argv[2]
    nota_fiscal = sys.argv[3]
    peso = sys.argv[4]

    # Carrega as tabelas que alimentam o sistema
    tabela = {"tabela1": {}, "tabela2": {}}
    tabela["tabela1"]["rota"] = ler_arquivo("tabela/rotas.csv")
    tabela["tabela1"]["preco_p_kg"] = ler_arquivo("tabela/preco_por_kg.csv")
    tabela["tabela2"]["rota"] = ler_arquivo("tabela2/rotas.tsv")
    tabela["tabela2"]["preco_p_kg"] = ler_arquivo("tabela2/preco_por_kg.tsv")

    transporte = Transporte(origem,destino,nota_fiscal,peso, tabela)

    frete = transporte.frete()
    transporte.format_output(frete)


