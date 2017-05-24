import sys
import os
from pybuilder.core import task, depends
from pybuilder.utils import execute_command


class PybResearchException(Exception):
    pass


def copy_env(target_dir):
    env = dict(os.environ)
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] += os.pathsep + target_dir
    else:
        env['PYTHONPATH'] = target_dir
    return env


@task('run_script', description='run script $PYB_SCRIPT in package context')
@depends('package')
def run_script(project, logger):
    scripts_directory = project.get_property('dir_dist_scripts')
    target_dir = project.expand_path('$dir_dist')
    target_script = os.getenv('PYB_SCRIPT')
    logger.info('Executing script %s in package context', target_script)
    env = copy_env(target_dir)
    logger.debug('Using environment:\n%s', env)
    if target_script:
        command = '{} {}'.format(
            sys.executable,
            os.path.join(target_dir, scripts_directory, target_script))
        if execute_command(command, env=env, shell=True):
            raise PybResearchException('Script failed')
    else:
        logger.error('PYB_SCRIPT variable is not set')
        raise PybResearchException('No PYB_SCRIPT variable set')
