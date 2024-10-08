from setuptools import setup, find_packages

setup(
    name='PuzzleGames',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/yourusername/PuzzleGames',
    license='MIT',
    author='thoma',
    author_email='your.email@example.com',
    description='A collection of puzzle games.',
    install_requires=[
        'playwright',
        'configparser',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
