from setuptools import find_packages
from setuptools import setup

#Add additional packages to requirements.txt to install
with open('requires.txt') as f:
    required = f.read().splitlines()

#change [template-adapter] to your adapter name and change version as needed
setup(
    name='[template-adapter]',
    namespace_packages=['activities_python'],
    python_requires='>=2.7.1',
    version="[1.0]",
    install_requires=required,
    description='[Template] Adapter',
    packages=find_packages(exclude=['tests', 'tests.*']),
    scripts=['worker/activities-worker'],
    zip_safe=True,
    setup_requires=['pytest-runner'],
    tests_require=['flake8', 'pytest', 'responses'],
)
