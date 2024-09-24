#!/usr/bin/env python3
import os
import re
import sys
import argparse
from collections import Counter


def carregar_blacklist(diretorio, verbose):
    blacklist_path = os.path.join(diretorio, 'blacklist.txt')
    if os.path.isfile(blacklist_path):
        if verbose:
            print(f"Carregando blacklist de {blacklist_path}")
        with open(blacklist_path, 'r', encoding='utf-8') as f:
            blacklist = set(line.strip().lower() for line in f if line.strip())
        if verbose:
            print(f"Blacklist carregada: {blacklist}")
        return blacklist
    if verbose:
        print("Nenhum arquivo blacklist.txt encontrado.")
    return set()


def contar_palavras(diretorio, blacklist, verbose):
    contador = Counter()

    # Percorre todos os arquivos no diretório
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            # Apenas arquivos .md (notas do Obsidian)
            if file.endswith('.md'):
                caminho_arquivo = os.path.join(root, file)
                if verbose:
                    print(f"Lendo arquivo {caminho_arquivo}")
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    texto = f.read()
                    # Remove caracteres especiais e divide em palavras
                    palavras = re.findall(r'\b\w+\b', texto.lower())
                    # Filtra as palavras que não estão na blacklist
                    palavras_filtradas = [
                        p for p in palavras if p not in blacklist]
                    contador.update(palavras_filtradas)
                    if verbose:
                        print(f"Contadas {len(palavras_filtradas)} palavras em {caminho_arquivo}")  # noqa: E501

    return contador


def main():
    parser = argparse.ArgumentParser(
        description="Contador de palavras para notas do Obsidian.")
    parser.add_argument("diretorio", nargs='?',
                        default=".", help="Caminho do diretório")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="Ativa modo verboso")
    args = parser.parse_args()

    diretorio = os.path.abspath(args.diretorio)
    verbose = args.verbose

    if os.path.isdir(diretorio):
        blacklist = carregar_blacklist(diretorio, verbose)
        palavras_comuns = contar_palavras(diretorio, blacklist, verbose)
        # Exibe as 10 palavras mais comuns
        for palavra, ocorrencias in palavras_comuns.most_common(10):
            print(f"{palavra}: {ocorrencias} ocorrências")
    else:
        print("O diretório informado não existe.")


if __name__ == "__main__":
    main()
