"""CharBlock provides the lowest level of abstraction for representing a
block of characters in the terminal as it represents a single character. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from worktoy.desc import Field
from worktoy.text import typeMsg

from consolatex import AbstractBlock


class Char(AbstractBlock):
  """CharBlock provides the lowest level of abstraction for representing a
  block of characters in the terminal as it represents a single
  character. """

  __inner_character__ = None

  char = Field()

  @char.GET
  def _getChar(self) -> str:
    if self.__inner_character__ is None:
      e = """CharBlock instance has not been initialized with a 
      character."""
      raise AttributeError(e)
    if isinstance(self.__inner_character__, str):
      return self.__inner_character__
    e = typeMsg('char', self.__inner_character__, str)
    raise TypeError

  def __init__(self, character: str) -> None:
    if len(character) - 1:
      e = """Received string with multiple characters, but CharBlock only
      requires a single character. """
      raise ValueError(e)
    self.__inner_character__ = character

  @classmethod
  def getBlockName(cls) -> str:
    """Getter-function for the block name. """
    return 'CHAR'

  @classmethod
  def getContentTypes(cls) -> list[type]:
    """This class uniquely cannot contain any other content blocks. """
    return [type(None), ]

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

  def render(self) -> str:
    """This class reimplements this method and returns the inner
    characters. """
    return self.char
