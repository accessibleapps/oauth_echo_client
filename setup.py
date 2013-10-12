from setuptools import setup

__version__ = 0.1
__doc__ = """Simple base client for OAuth Echo services."""

setup(
 name = 'oauth_echo_client',
 version = __version__,
 description = __doc__,
 py_modules = ['oauth_echo_client'],
 install_requires = [
  'requests',
  'oauth',
 ],
 classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Topic :: Software Development :: Libraries',
 ],
)
