"""Confere uma pasta de mockups HTML estáticos.

- todo link e todo recurso local (href, src) aponta para um arquivo que existe;
- nenhum recurso vem de fora (http, https ou //), salvo os links de texto do índice;
- toda tela, menos o índice, tem ao menos um link para outra tela;
- toda tela é alcançável a partir do index.html (por link ou iframe).

Uso: python3 conferir_mockups.py <pasta dos mockups>
Sai com 1 e lista os problemas, ou com 0 e um resumo.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Refs(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.recursos: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for nome, valor in attrs:
            if not valor:
                continue
            if tag == "a" and nome == "href":
                self.links.append(valor)
            elif (tag == "iframe" and nome == "src") or (tag != "a" and nome in ("href", "src")):
                self.recursos.append(valor)
            if tag == "iframe" and nome == "src":
                self.links.append(valor)


def externo(url: str) -> bool:
    return urlsplit(url).scheme in ("http", "https") or url.startswith("//")


def local(url: str) -> str | None:
    partes = urlsplit(url)
    if partes.scheme or url.startswith("//") or not partes.path:
        return None
    return unquote(partes.path)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    pasta = Path(sys.argv[1]).resolve()
    telas = sorted(pasta.glob("*.html"))
    indice = pasta / "index.html"
    problemas: list[str] = []
    if not indice.is_file():
        problemas.append("falta o index.html")
    grafo: dict[Path, set[Path]] = {}
    for tela in telas:
        refs = Refs()
        refs.feed(tela.read_text(encoding="utf-8"))
        nome = tela.name
        destinos: set[Path] = set()
        for url in refs.links + refs.recursos:
            caminho = local(url)
            if caminho is None:
                if externo(url) and (url in refs.recursos or tela != indice):
                    problemas.append(f"{nome}: recurso ou link externo {url}")
                continue
            alvo = (tela.parent / caminho).resolve()
            if not alvo.exists():
                problemas.append(f"{nome}: {url} não existe")
            elif alvo.suffix == ".html" and alvo.parent == pasta and alvo != tela:
                destinos.add(alvo)
        grafo[tela] = destinos
        if tela != indice and not destinos:
            problemas.append(f"{nome}: tela sem saída (nenhum link para outra tela)")
    if indice.is_file():
        vistos, fila = {indice}, [indice]
        while fila:
            for vizinho in grafo.get(fila.pop(), ()):
                if vizinho not in vistos:
                    vistos.add(vizinho)
                    fila.append(vizinho)
        for tela in telas:
            if tela not in vistos:
                problemas.append(f"{tela.name}: o index.html não chega a esta tela")
    if problemas:
        print("\n".join(f"✗ {p}" for p in problemas))
        return 1
    print(f"✓ {len(telas)} arquivos HTML conferidos em {pasta.name}/: links, saídas e alcance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
