from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='git_set_commit_status',
      version='0.1',
      description='Set commit status of pull/push/merge request.',
      long_description=long_description,
      url='https://github.com/Nebojsa92/git_set_commit_status',
      author='Nebojša Stevanović',
      author_email='nebojsa992@gmail.com',
      license='GNU GPLv3',
      packages=['git_set_commit_status'],
      zip_safe=False)