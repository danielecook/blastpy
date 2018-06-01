import setuptools
from packagename import __version__


setuptools.setup(name='py-boilerplate',
                 version=__version__,
                 description='Python Package Boilerplate',
                 long_description=open('README.md').read().strip(),
                 author='Package Author',
                 author_email='you@youremail.com',
                 url='http://path-to-my-packagename',
                 py_modules=['packagename'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='boilerplate package',
                 classifiers=['Packages', 'Boilerplate'])
