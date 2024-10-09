"""Word represents a single word and consists of Char instances."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from consolatex import AbstractBlock, Char


class Word(AbstractBlock):
  """Word represents a single word and consists of Char instances."""

  def __init__(self, word: str) -> None:
    for character in word:
      self.append(Char(character))

  @classmethod
  def getBlockName(cls) -> str:
    """Getter-function for the block name. """
    return 'WORD'

  @classmethod
  def getContentTypes(cls) -> list[type]:
    """Subclasses must provide a list of types that are allowed as content
    in the block. The types must be subclasses of AbstractBlock. This
    implies the principle that lower order types should be defined before
    higher order types. """
    return [Char, ]

  @classmethod
  def getPrelude(cls) -> Self:
    """Subclasses must provide prelude that precedes instances of itself. """
    return ''

  @classmethod
  def getSeperator(cls) -> str:
    """Getter-function for what will separate each content block when
    instances of this class is rendered."""
    return ''

  @classmethod
  def getPostlude(cls) -> Self:
    """Subclasses must provide postlude that follows instances of itself. """
    return ''
