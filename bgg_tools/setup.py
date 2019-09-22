from setuptools import setup

setup(name='bgg_tools',
      version='0.1',
      description='Tools for utilizing BGG APIs from python',
      url='http://github.com/shelmich/bgg_tools',
      author='Sam Helmich',
      author_email='sam.helmich@gmail.com',
      license='MIT',
      packages=['bgg_tools'],
      install_requires=[
            'requests',
            'ElementTree'
      ],
      zip_safe=False)