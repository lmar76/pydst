from setuptools import setup


def get_version(filename):
    """Read version info from file without importing it."""
    for line in open(filename):
        if '__version__' in line:
            if '"' in line:
                # __version__ = "0.9"
                return line.split('"')[1]
            elif "'" in line:
                # __version__ = '0.9'
                return line.split("'")[1]


setup(
    name='pydst',
    version = get_version('pydst.py'),
    py_modules=['pydst'],
    description='Python library for Dst index files.',
    author='Luca Mariani',
    author_email='lmar76@gmail.com',
    url='https://bitbucket.org/lmar76/pydst/overview',
    keywords=['dst'],
    requires=['numpy']
)
