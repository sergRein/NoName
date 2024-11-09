from setuptools import setup, find_packages

setup(
    name='pip_boy_assistant',
    version='1.0.0',
    author='No Idea Crew',
    author_email='example@example.com',
    description='Personal assistant app similar to Pip-Boy from the Fallout universe',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sergRein/NoName',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'pipboy-assistant=main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
