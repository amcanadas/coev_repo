from setuptools import setup
import os


setup(name='YourAppName',
      version='0.1.0',
      description='OpenShift App',
      author='Your Name',
      author_email='example@example.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=open('%s/requirements.txt' % os.environ.get('OPENSHIFT_REPO_DIR')).readlines(),
)
