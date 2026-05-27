"""
WSGI entry point for PythonAnywhere.

In the PythonAnywhere web app settings, set:
  Source code:   /home/YOUR_USERNAME/tg-todo
  Working dir:   /home/YOUR_USERNAME/tg-todo
  WSGI file:     /home/YOUR_USERNAME/tg-todo/wsgi.py
"""
import sys
import os

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from webhook_server import app as application  # noqa: F401
