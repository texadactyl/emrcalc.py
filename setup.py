"""
setup.py -- setup script for installing a python3-pip package.
"""
# To increment version
# Check you have ~/.pypirc filled in
# git tag x.y.z
# git push && git push --tags
# rm -rf dist; python3 setup.py sdist bdist_wheel
# auditwheel repair dist/*.whl -w dist/ (Linux)
# TEST: twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# twine upload dist/*


from setuptools import setup, find_packages

__version__ = "1.4.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.readlines()

entry_points = {
    'console_scripts' :
        ['emrcalc = emrcalc.emrcalc_main:main']
}


setup(
    name="emrcalc",
    version=__version__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GNU General Public License Version 3",
    install_requires=install_requires,
    entry_points=entry_points,
    packages=find_packages(),
    author="Richard Elkins",
    author_email="richard.elkins@gmail.com",
    description="Electromagnetic Radiation Calculator",
    keywords="astronomy chemistry physics",
    url="https://github.com/texadactyl/emrcalc",
    zip_safe=False,
    options={"bdist_wheel": {"universal": "1"}},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
