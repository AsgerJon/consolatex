"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

import worktoy
from worktoy import text

import consolatex
from yolo import yolo


def tester00() -> int:
  """Hello world!"""
  stuff = [os, sys, worktoy, consolatex, text]
  for item in stuff:
    print(item)
  else:
    return 0


if __name__ == '__main__':
  yolo(tester00)
