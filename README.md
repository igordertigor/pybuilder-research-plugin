# pybuilder-research-plugin

This repository provides a plugin to support research handling of
[pybuilder](http://pybuilder.github.io/) repositories. There are some peculiar
differences between writing production code and research code. In particular,
research code often consists of a set of scripts that need to be run once to
generate a certain result and afterwards only the result counts (and the script
is needed for reproducability).


## Why use pybuilder for research code?

pybuilder unifies many typical development tasks including running unit tests
and analyzing coverage. Although unit-tests are not particularly common in
research code, they are very helpful for those parts of the code that are being
used repeatedly. I have therefore often maintained a python package to hold
those parts of the code that are used repeatedly and that form kind of the
"backbone" of the project. On top of that, I had a bunch of scripts to flexibly
put those parts together. For the python package, I like to use pybuilder to
simplify those typical development tasks.


## What does the plugin provide?

If I use pybuilder to manage the python package for my research code, it
becomes quite unflexible to run my scripts with the latest changes in the
package included. I often caught myself running commands like this one:
```
PYTHONPATH=target/dist/cool-research-1.0dev0/ python target/dist/cool-research-1.0dev0/scripts/convert_data.py
```

However, I usually work on one of the scripts. Pybuilder research simplifies
this as:
```
export PYB_SCRIPT=convert_data.py
pyb run_script
```
This is for one less error prone and for two less typing.

Furthermore, the plugin provides a command (`start_figure`) to create a simple template for
creating figure scripts. This can be controlled by the following two
properties:

- `use_seaborn`: boolean for whether to include
  [seaborn](https://seaborn.pydata.org) (the default), or not.
- `new_figure_name`: The filename in which to create the new figure. This
  will be created in your scripts folder and you should probably rename
  the file to something that describes what your figure shows. Default is
  `figure.py`.

In the future, pybuilder-research-plugin might contain other tasks such as
compiling a paper or potentially integration of experiment tracking tools such
as [sumatra](https://pythonhosted.org/Sumatra/) or
[sacred](https://github.com/IDSIA/sacre://github.com/IDSIA/sacred). Yet, these
will evolve as I feel they are needed (or someone sends me a pull request).

## How do I install it?

Just add it to your `build.py`:
```python
use_plugin('pypi:pybuilder_research_plugin')
```
