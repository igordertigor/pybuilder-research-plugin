from pybuilder.core import use_plugin, init, Author
from pybuilder.vcs import count_travis

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "pybuilder-research-plugin"
default_task = "publish"
version = count_travis()
authors = [Author('Ingo Fruend', 'github@ingofruend.net')]
requires_python = '>=2.7,!=3.0,!=3.1,!=3.2'
url = 'https://github.com/igordertigor/pybuilder-research-plugin'


@init
def set_properties(project):
    pass
