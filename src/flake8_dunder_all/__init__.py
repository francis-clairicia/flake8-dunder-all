# -*- coding: Utf-8 -*-

from __future__ import annotations

__all__ = ["DunderAll"]

__author__ = "FrankySnow9"
__contact__ = "clairicia.rcj.francis@gmail.com"
__copyright__ = "Copyright (c) 2023, Francis Clairicia-Rose-Claire-Josephine"
__credits__ = ["FrankySnow9"]
__deprecated__ = False
__email__ = "clairicia.rcj.francis@gmail.com"
__license__ = "MIT"
__maintainer__ = "FrankySnow9"
__status__ = "Development"
__version__ = "0.1.0"

import ast
from dataclasses import dataclass
from typing import ClassVar, Generator, NamedTuple


class Error(NamedTuple):
    lineno: int
    col: int
    message: str
    type: type


@dataclass
class DunderAll:
    name: ClassVar[str] = "dunder-all"
    version: ClassVar[str] = __version__

    tree: ast.Module

    def run(self) -> Generator[Error, None, None]:
        tree: ast.Module = self.tree
        misplaced_import_lines: list[tuple[int, int]] = []
        for node in tree.body:
            match node:
                case ast.ImportFrom(module="__future__"):
                    continue
                case ast.Import() | ast.ImportFrom():
                    misplaced_import_lines.append((node.lineno, node.col_offset))
                    continue
                case ast.Assign(targets=[ast.Name(id="__all__")]) | ast.AnnAssign(target=ast.Name(id="__all__")):
                    break
                case _:
                    continue
        else:  # __all__ not found
            yield Error(1, 0, DALL001, type(self))
            return
        for lineno, col_offset in misplaced_import_lines:
            yield Error(
                lineno,
                col_offset,
                DALL002,
                type(self),
            )


DALL001 = "DALL001 There is no __all__ defined"
DALL002 = "DALL002 'import' statement before __all__ declaration"
