from setuptools import setup

setup(
    name='IoT_MemeGenerator',
    version='0.1',
    description="IoT Meme Generator makes memes",
    license="GPLv3+",
    author="Matthew Meza",
    author_email="mfmeza231@gmail.com",
    packages=['memeify'],
    package_data={
        'memeify': ['*.txt', '*.otf']
    },
    setup_requires=['lambda_setuptools'],
    lambda_function="memeify.lambda:lambda_handler",
    install_requires=[
        'requests',
        'markovify',
        'Pillow',
        'flickrapi',
        'psycopg2-binary'
    ]
)
