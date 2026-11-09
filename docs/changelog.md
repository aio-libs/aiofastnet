# Changelog

```{eval-rst}

.. MyST doesn't support the "only" directive correctly. It always evaluates to
.. true. Still the case with myst-parser 5.1.0.
..
.. But if we drop into sphinx eval-rst, it works fine.
.. We then need to include our draft changelog content as markdown.
..
.. We're making a "MyST sandwich", with RST for the `{only}` directive in the
.. middle.
..
.. Including a Markdown file from RST with `:parser:` is documented here:
.. https://myst-parser.readthedocs.io/en/latest/faq/index.html#include-markdown-files-into-an-rst-file

.. only:: not is_release

    .. include:: changelog.d/.draft_changelog_partial.md
        :parser: myst_parser.sphinx_

```

```{include} ../CHANGELOG.md
:start-after: <!-- towncrier release notes start -->
```
