from setuptools import find_packages, setup


requirements = [r for r in open('requirements.txt', 'r').read().splitlines()]

setup(
    name='service_lib',
    version='0.0.4',
    license='BSD',
    description='Library dependency microservice.',
    long_description_content_type='text/markdown',
    author='jeager',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8.9",
    zip_safe=False
)
