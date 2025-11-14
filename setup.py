from setuptools import setup, find_packages

def read_requirements():
    with open("pyproject.toml", "r") as f:
        lines = f.readlines()
    deps = [line.strip().strip('",') for line in lines if line.strip().startswith('"')]
    return deps


setup(
    name='msml_terptracker',
    version='1.0.0',
    packages=find_packages(include=['terptracker', 'terptracker.*']),
    install_requires=read_requirements()
)