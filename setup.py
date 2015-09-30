from setuptools import setup, find_packages

setup(name='musicgrid',
      packages=find_packages(),
      install_requires=[
          'morepath',
          'pylast',
          'sqlalchemy',
          'more.transaction',
          'zope.sqlalchemy',
          'spotipy',
      ],
      entry_points={
         'console_scripts': [
             'musicgrid-start = musicgrid.main:main',
             'musicgrid-shell = musicgrid.main:shell',
             'musicgrid-update = musicgrid.lastfm:update',
          ]
      })
