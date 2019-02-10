from setuptools import setup

setup(name='maynou',
      version='0.1',
      description='Python module to control Maynou Electronic loads',
      url='https://github.com/danielcrowley/OpenTestRig-ElectronicLoad-Maynou',
      author='Daniel Crowley',
      author_email='crowley.daniel@gmail.com',
      license='MIT',
      packages=['maynou'],
      install_requires=[
        'minimalmodbus'
    ])
