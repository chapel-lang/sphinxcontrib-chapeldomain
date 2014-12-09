from setuptools import setup, find_packages

with open('README.rst') as fp:
    long_desc = fp.read()

setup(
    name='sphinxcontrib-chapeldomain',
    version='0.0.1',
    url='',
    download_url='',
    license='Apache License v2.0',
    author='Chapel Team',
    author_email='chapel-developers@lists.sourceforge.net',
    description='Chapel domain for Sphinx',
    long_description=long_desc,
    zip_safe=False,  # TODO: Can this be True? (thomasvandoren, 2014-12-09)
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Sphinx>=1.0',
    ],
    namespace_packages=['sphinxcontrib']
)
