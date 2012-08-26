from distutils.core import setup
setup(name='django-contactform',
    version='0.1.0',
    author='Aleksander Zdyb',
    author_email='azdyb@live.com',
    description='Generic, class-based contact form for Django',
    long_description=open('README.rst').read(),
    license='BSD',
    url='http://github.com/ojo/django-contactform',
    packages=["contactform"],
    package_data={
        'contactform': [
            'locale/*/LC_MESSAGES/*',
        ],
    },
    classifiers=['Development Status :: 2 - Pre-Alpha',
                'Environment :: Web Environment',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Utilities'],
)
