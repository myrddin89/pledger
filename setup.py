from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()
        

setup(
    name='pledger',
    version="0.1.0",
    license='MIT',
    description='Ledger CLI helper tool',
    long_description=readme(),
    url='https://github.com/myrddin89/pledger',
    author='Nicola Mosco',
    author_email='nicola.mosco@gmail.com',
    packages=['pledger'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Accounting',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    entry_points={
        'console_scripts': ['pledger=pledger.pledger:main']
    },
    install_requires=[
        'docopt',
        'pyyaml'
    ]
)
