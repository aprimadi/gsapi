#import wingdbstub
import time
import os, sys
from fabric.api import local, cd, run, env, sudo, require
from gsapi.settings import Config

fab            = Config.FABRIC['live']

env.hosts      = fab['HOSTS']
env.user       = fab['ADMIN_USER']
env.admin_     = fab['ADMIN_USER']
env.admin_user = fab['ADMIN_USER']

def hello():
    print("Hello world!")

def r():
    # symlink convenience
    # ln -s /home/flt/django/projects/flt/ /home/flt/dj
    run('cd C:\Users\Larry\__prjs\flt; ls')


#from fabric.decorators import runs_once

from fabric.contrib.console import confirm

# see: http://blog.tplus1.com/index.php/2010/12/31/how-to-restart-a-gunicorn-server-from-vim/
def reload_code():
    with cd(fab['PROJECT_ROOT']):
        sudo('kill -HUP `cat gunicorn.pid`')

def start_gunicorn():
    with cd(fab['PROJECT_ROOT']):
        sudo('python manage.py run_gunicorn -c gunicorn.conf.py --traceback 0.0.0.0:8001')

def stop_gunicorn():
    with cd(fab['PROJECT_ROOT']):
        sudo('kill `cat gunicorn.pid`')


def restart_gunicorn():
    with cd(fab['PROJECT_ROOT']):
        sudo('kill `cat gunicorn.pid`')
        sudo('python manage.py run_gunicorn -c gunicorn.conf.py --traceback 0.0.0.0:8001')

def reload_nginx_conf():
    sudo('/etc/init.d/nginx check')
    sudo('/etc/init.d/nginx reload')

#@run_once
def commit(msg):
    with cd(os.path.abspath(os.path.dirname(__file__))):
        local('git add .')
        local('git commit -am"%s"' % msg)
        local('git push origin master') # push local to repository

def update_remote():
    env.user = fab['WEB_USER']

    with cd(fab['PROJECT_ROOT']):
        run('git pull origin master') # pull from repository to remote
        run('python manage.py collectstatic -v0 --noinput')

def restart():
    sudo('supervisorctl restart ourfield')
    # sudo /etc/init.d/nginx restart
    sudo('/etc/init.d/nginx restart')

# def deploy(push_code=False):
def deploy(msg="No Msg"):
    #if push_code:
        #commit_code()
    commit(msg)
    update_remote()
    #restart()
    print "Perhaps:"
    print "fab reload_code"


def pushpull():
    local('git push') # runs the command on the local environment
    run('cd /path/to/project/; git pull') # runs the command on the remote environment
