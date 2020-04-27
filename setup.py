from setuptools import setup

with open('library/version.txt') as f:
    version = [x.strip() for x in f.readlines()][0]

if not version:
    exit(1)

setup(name='library',
      version=version,
      description='liquidnet exercise',
      url='http://github.com/hugoleeney/liquidnet_exercize',
      license='None',
      packages=["library"],
      install_requires=[
            'certifi==2020.4.5.1',
            'chardet==3.0.4',
            'click==7.1.2',
            'Flask==1.1.2',
            'Flask-SQLAlchemy==2.4.1',
            'formatizer==0.1.1',
            'future==0.18.2',
            'idna==2.9',
            'itsdangerous==1.1.0',
            'Jinja2==2.11.2',
            'MarkupSafe==1.1.1',
            'six==1.14.0',
            'SQLAlchemy==1.3.16',
            'urllib3==1.25.9',
            'Werkzeug==1.0.1',
            'ww==0.2.1'
      ],
      zip_safe=False)

