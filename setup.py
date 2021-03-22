from setuptools import setup

__version__ = 0.2
__doc__ = """Simple base client for OAuth Echo services."""

setup(
 name = 'oauth_echo_client',
 version = __version__,
 description = __doc__,
 py_modules = ['oauth_echo_client'],
 install_requires = [
  'requests',
  'python-oauth2',
 ],
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Topic :: Software Development :: Libraries',
 ],
)
