# py2exe setup.py file to create an executable from dataCompletedScript.py
# @author: Aaron Ponti

# Needed imports
from distutils.core import setup
import py2exe

# Create a console executable from dataCompletedScript.py
setup(name='DataCompletedScript',
      version='0.2.0',
      author='Aaron Ponti',
      author_email='aaron.ponti@bsse.ethz.ch',
      console=['src/dataCompletedScript.py'])
