# setup.py

from setuptools import setup, find_packages
import os

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='EyeBreakReminder',
    version='1.0.0',
    description='A desktop application to remind users to take eye breaks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Artem Tarasiuk',
    author_email='artemtotal@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5>=5.15.0',
        'pygame>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'eye-break-reminder=eye_break_reminder.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
