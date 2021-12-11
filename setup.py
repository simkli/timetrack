from setuptools import setup

setup(
    name='TimeTrack',
    version='1.0.0',
    packages=['timetrack'],
    url='https://github.com/simkli/timetrack',
    license='AGPLv3',
    author='Simon Klimek',
    author_email='project@simkli.de',
    description='Timetracker using Google Calendar',
    install_requires=[
        "pandas~=1.3.1",
        "seaborn~=0.11.2",
        "matplotlib~=3.4.3",
        "google-api-python-client~=2.15.0",
        "google-auth-httplib2~=0.1.0",
        "google-auth-oauthlib~=0.4.5",
    ],
    entry_points={
        'console_scripts': [
            'timetrack = timetrack.cli:main'
        ]
    },
)
