from setuptools import setup, find_namespace_packages

setup(
    name='PuzzleGames',
    version='1.0.0',
    packages=find_namespace_packages(include=['Domain', 'Domain.*', 'Utils', 'Utils.*']),
    url='https://github.com/newtomsoft/Puzzle',
    license='MIT',
    author='thoma',
    author_email='thomas@newtomsoft.fr',
    description='A collection of puzzle games.',
    install_requires=[
        'rebrowser-playwright',
        'configparser',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
