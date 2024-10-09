"""Letter enumerates the letters of the alphabet."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNumSpace, KeeNumObject, KeeNumMeta, auto


class LetterSpace(KeeNumSpace):
  """Allows case sensitivity"""

  def __explicit_set__(self, key: str, value: object) -> None:
    """The __explicit_set__ method is invoked by __setitem__."""
    if key == '__init__':
      e = """The __init__ method is reserved for KeeNum classes!"""
      raise AttributeError(e)
    if isinstance(value, KeeNumObject):
      # key = key.upper()  # This line is removed
      entries = self.getKeeNumEntries()
      value._pvtVal = ord(value.value)  # Sets the private value to ord
      value.name = key
      if value.value is None:
        value.value = key
      self.__keenum_entries__ = [*entries, value]


class LetterMeta(KeeNumMeta):
  """Uses LetterSpace instead of KeeNumSpace"""

  @classmethod
  def __prepare__(mcls, name: str, _, **kwargs) -> KeeNumSpace:
    """The __prepare__ method is invoked before the class is created."""
    return LetterSpace(mcls, name, (), **kwargs)


class Letter(metaclass=LetterMeta):
  """Letter enumerates the letters of the alphabet."""

  AUpper = auto('A')
  BUpper = auto('B')
  CUpper = auto('C')
  DUpper = auto('D')
  EUpper = auto('E')
  FUpper = auto('F')
  GUpper = auto('G')
  HUpper = auto('H')
  IUpper = auto('I')
  JUpper = auto('J')
  KUpper = auto('K')
  LUpper = auto('L')
  MUpper = auto('M')
  NUpper = auto('N')
  OUpper = auto('O')
  PUpper = auto('P')
  QUpper = auto('Q')
  RUpper = auto('R')
  SUpper = auto('S')
  TUpper = auto('T')
  UUpper = auto('U')
  VUpper = auto('V')
  WUpper = auto('W')
  XUpper = auto('X')
  YUpper = auto('Y')
  ZUpper = auto('Z')
  AEUpper = auto('Æ')
  OEUpper = auto('Ø')
  AAUpper = auto('Å')

  #  Lowercase:

  ALower = auto('a')
  BLower = auto('b')
  CLower = auto('c')
  DLower = auto('d')
  ELower = auto('e')
  FLower = auto('f')
  GLower = auto('g')
  HLower = auto('h')
  ILower = auto('i')
  JLower = auto('j')
  KLower = auto('k')
  LLower = auto('l')
  MLower = auto('m')
  NLower = auto('n')
  OLower = auto('o')
  PLower = auto('p')
  QLower = auto('q')
  RLower = auto('r')
  SLower = auto('s')
  TLower = auto('t')
  ULower = auto('u')
  VLower = auto('v')
  WLower = auto('w')
  XLower = auto('x')
  YLower = auto('y')
  ZLower = auto('z')
  AELower = auto('æ')
  OELower = auto('ø')
  AALower = auto('å')

  def __int__(self, ) -> int:
    """Returns the value of the letter as an integer."""
    return ord(self.value)
