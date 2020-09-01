from setuptools import setup, find_packages


setup(
    name='factsheet',
    description='Stock factsheet command-line tool',
    version='1.0',
    author='NB',
    python_requires='>=3.6',
    packages=['factsheet'],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    install_requires = [
        'async-timeout==3.0.1',
        'attrs==20.1.0',
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'colorama==0.4.3',
        'cycler==0.10.0',
        'idna==2.10',
        'kiwisolver==1.2.0',
        'matplotlib==3.3.1',
        'millify==0.1.1',
        'multidict==4.7.6',
        'numpy==1.19.1',
        'Pillow==7.2.0',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'requests==2.24.0',
        'six==1.15.0',
        'termplotlib==0.3.2',
        'urllib3==1.25.10',
        'yarl==1.5.1'
    ],
    entry_points={
	'console_scripts': [
            'factsheet=factsheet.factsheet:main'
	]
    }
)
