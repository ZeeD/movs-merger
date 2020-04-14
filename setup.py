import setuptools


setuptools.setup(
    name='movs-merger',
    version='0.0.0',
    url='http://www.example.com',
    author='Vito De Tullio',
    author_email='vito.detullio@gmail.com',
    py_modules=setuptools.find_packages(),
    extra_require={
        'dev': [
            'distutil'
        ]
    },
    package_dir={'': 'src'},
    package_data={
        'movs': ['py.typed'],
    })
