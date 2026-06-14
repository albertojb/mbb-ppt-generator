# Copyright 2024-2026 Kaku Li (https://github.com/likaku)
# Licensed under the Apache License, Version 2.0 — see LICENSE and NOTICE.
# Originally part of "Mck-ppt-design-skill"; renamed to mbb_ppt in this
# derivative work and bundled under the upstream Apache 2.0 license.
# NOTICE: This file must be retained in all copies or substantial portions.
#
"""MBB PPT Generator — High-level Layout Function Library.

Public alias: ExecEngine. Underlying class: MbbEngine.

Usage::

    from mbb_ppt import MbbEngine as ExecEngine
    eng = ExecEngine(total_slides=10)
    eng.cover(title='My Title', subtitle='Subtitle')
    eng.toc(items=[('1', 'Topic', 'Description'), ...])
    eng.save('output/my_deck.pptx')
"""
from .engine import MbbEngine
from .constants import *
from .review import SlideReviewer, AutoFixPipeline, review, autofix

ExecEngine = MbbEngine

__version__ = '0.7.0'
