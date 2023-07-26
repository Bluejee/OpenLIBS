import setuptools

with open('README.md', 'r') as f:
    long_disc = f.read()

setuptools.setup(
    include_package_data=True,
    name='OpenLIBS',
    version='0.1.0',
    author='Balakrishna Prabhu B N',
    author_email='balakrishnaprabhu1999@gmail.com',
    description='OpenLIBS is a package that provides functionality to analyse Laser Induced Breakdown Spectroscopic Spectras',
    long_description=long_disc,
    long_description_content_type="text/markdown",
    keywords=['analysis', 'LIBS', 'spectroscopy', 'database', 'laser', 'Physics', 'Computation'],
    url='https://github.com/Bluejee/OpenLIBS',
    packages=['OpenLIBS'],
    install_requires=['pandas>=1.4.0'],
    python_requires='>=3.7',
    license='GPL-3.0-or-later',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ]
)
