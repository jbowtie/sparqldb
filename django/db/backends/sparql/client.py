from django.conf import settings
import os

def runshell():
    args = ['sparqldb']
    args += ['/home/jbowtie/tmp/' + settings.DATABASE_NAME]
    os.execvp('sparqldb', args)

