Example `reStructuredText` document
===================================

RST syntax is still allowed when using `myst-parser`, either in code blocks in markdown
files or as entire files like this one.

My nifty `reStructuredText` subsection title
--------------------------------------------

Some **text**!

.. warning::
    Here's my admonition content



.. _section_two:

Here's another `reStructuredText` section
-----------------------------------------

.. This comment won't make it into the outputs!

And here's :ref:`a reference to this section <section-two>`.
I can also reference the section :ref:`section-two` without specifying my title.


.. note::  This is a **note** box.

.. mermaid::

   sequenceDiagram
      participant Alice
      participant Bob
      Alice->John: Hello John, how are you?
      loop Healthcheck
          John->John: Fight against hypochondria
      end
      Note right of John: Rational thoughts <br/>prevail...
      John-->Alice: Great!
      John->Bob: How about you?
      Bob-->John: Jolly good!
