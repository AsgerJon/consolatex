"""AbstractBlock provides an abstract baseclass for text blocks. The text
representation splits the text into blocks of different types and
hierarchies, for example Chapter > Section > Paragraph, but also for other
block types such as Quote, Graphic (limited in terminal though) and
importantly something like Code."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self
from abc import abstractmethod

from worktoy.base import BaseObject, overload
from worktoy.desc import AttriBox, THIS
from worktoy.parse import maybe
from worktoy.text import typeMsg


class AbstractBlock(BaseObject):
  """AbstractBlock provides an abstract baseclass for text blocks. The text
  representation splits the text into blocks of different types and
  hierarchies, for example Chapter > Section > Paragraph, but also for other
  block types such as Quote, Graphic (limited in terminal though) and
  importantly something like Code."""

  __content_blocks__ = None
  __iter_contents__ = None

  label = AttriBox[str]()

  @classmethod
  @abstractmethod
  def getBlockName(cls) -> str:
    """Subclasses must provide a unique name. This will be used in compiling
    the coded text. The syntax is:
    {{BEGIN}::{<name>}}  # Begins block of type <name> where name is
                         # returned by this method.
    ...  # chapter content
    {{END}::{<name>}}    # Ends block of type <name>"""

  @classmethod
  @abstractmethod
  def getContentTypes(cls) -> list[type]:
    """Subclasses must provide a list of types that are allowed as content
    in the block. The types must be subclasses of AbstractBlock. This
    implies the principle that lower order types should be defined before
    higher order types. """

  @classmethod
  @abstractmethod
  def getPrelude(cls) -> Self:
    """Subclasses must provide prelude that precedes instances of itself. """

  @classmethod
  @abstractmethod
  def getSeperator(cls) -> str:
    """Getter-function for what will separate each content block when
    instances of this class is rendered."""

  @classmethod
  @abstractmethod
  def getPostlude(cls) -> Self:
    """Subclasses must provide postlude that follows instances of itself. """

  @classmethod
  def validateBlock(cls, block: AbstractBlock) -> None:
    """Validates that the block belongs to a content type of this class"""
    contentTypes = cls.getContentTypes()
    if not contentTypes:
      e = """The content types list is empty!"""
      raise AttributeError(e)
    if not isinstance(block, (*contentTypes,)):
      e = typeMsg('block', block, contentTypes[0])
      raise TypeError(e)

  def getContent(self) -> list[AbstractBlock]:
    """Returns the content list."""
    return maybe(self.__content_blocks__, [])

  def __len__(self, ) -> int:
    """Returns the number of content blocks"""
    return len(self.getContent())

  def __abs__(self, ) -> int:
    """Returns the number of characters included"""
    return sum([abs(block) for block in self])

  def _rollIndex(self, index: int) -> int:
    """Rolls the index to a valid index"""
    while index < 0:
      index += len(self)
    if index < len(self):
      return index
    raise IndexError(index)

  def append(self, block: AbstractBlock) -> None:
    """Appends a block to the content list."""
    self.validateBlock(block)
    existing = self.getContent()
    self.__content_blocks__ = [*existing, block]

  def insert(self, block: AbstractBlock, after: int) -> None:
    """Inserts the given block after the first 'after' number of existing
    blocks"""
    self.validateBlock(block)
    existing = self.getContent()
    if after:
      preBlocks = existing[:after]
      postBlocks = existing[after:]
    else:
      preBlocks = []
      postBlocks = existing
    self.__content_blocks__ = [*preBlocks, block, *postBlocks]

  @overload(THIS)
  def remove(self, block: AbstractBlock) -> Self:
    """Removes the block from the content list."""
    existing = self.getContent()
    newContent = []
    for item in existing:
      if item is not block:
        newContent.append(block)
    self.__content_blocks__ = newContent
    return block

  @overload(int)
  def remove(self, index: int) -> AbstractBlock:
    """Removes the block at the given index from the content list."""
    if self.__content_blocks__ is None:
      raise IndexError(index)
    return self.__content_blocks__.pop(self._rollIndex(index))

  @overload(str)
  def remove(self, label: str) -> AbstractBlock:
    """Removes the block with the given label from the content list."""
    existing = self.getContent()
    for (i, block) in enumerate(existing):
      if block.label == label:
        return self.remove(i)
    raise KeyError(label)

  def __iter__(self, ) -> AbstractBlock:
    """Implementation of iteration"""
    self.__iter_contents__ = [*self.getContent(), ]
    return self

  def __next__(self, ) -> AbstractBlock:
    """Implementation of iteration"""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __setitem__(self, key: object, block: AbstractBlock) -> None:
    """Sets the block with the given key"""
    existing = self.getContent()
    if isinstance(key, int):
      existing[self._rollIndex(key)] = block
      index = self._rollIndex(key)
      if index:
        preBlocks = existing[:index]
        postBlocks = existing[index + 1:]
      else:
        preBlocks = []
        postBlocks = existing[1:]
      self.__content_blocks__ = [*preBlocks, block, *postBlocks]
    elif isinstance(key, str):
      for (i, block) in enumerate(existing):
        if block.label == key:
          return self.__setitem__(i, block)
      raise KeyError(key)
    else:
      e = typeMsg('key', key, str)
      raise TypeError(e)

  def __getitem__(self, key: object) -> AbstractBlock:
    """Retrieves the block identified by the key"""
    existing = self.getContent()
    if isinstance(key, int):
      index = self._rollIndex(key)
      return existing[index]
    if isinstance(key, str):
      for block in existing:
        if block.label == key:
          return block
      raise KeyError(key)
    e = typeMsg('key', key, int)
    raise TypeError(e)

  def __delitem__(self, key: object) -> AbstractBlock:
    """Deletes and returns the block at the given key"""
    if isinstance(key, int):
      return self.remove(self._rollIndex(key))
    if isinstance(key, str):
      return self.remove(key)
    e = typeMsg('key', key, int)
    raise TypeError(e)

  def render(self) -> str:
    """Renders the block and its content as a string."""
    seperator = self.getSeperator()
    prelude = self.getPrelude()
    postlude = self.getPostlude()
    inner = seperator.join([block.render() for block in self])
    return ''.join([prelude.render(), inner, postlude.render()])
