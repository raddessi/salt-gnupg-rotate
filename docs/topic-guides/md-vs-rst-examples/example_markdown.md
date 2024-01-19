# Example Markdown document

Using [MyST](https://myst-parser.readthedocs.io/en/latest/index.html) makes it
possible to use both `.md` and `.rst` files in documentation!

## My nifty Markdown subsection title

Some **text**!

```{admonition} Here's my title
:class: warning

Here's my admonition content
```

(section-two)=

## Here's another Markdown section

And some more content.

% This comment won't make it into the outputs! And here's
{ref}`a reference to this section <section-two>`. I can also reference the
section {ref}`section-two` without specifying my title.

```{note}
And here's a note!
```

:::{note} And here's a note with a colon fence! :::

And finally, here's a cool mermaid diagram!

```{mermaid}
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
```
