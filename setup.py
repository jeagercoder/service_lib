from setuptools import find_packages, setup

setup(
    name='service_lib',
    version='0.0.1',
    license='BSD',
    description='Library dependency microservice.',
    long_description_content_type='text/markdown',
    author='jeager',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=["django==4.1.7", "djangorestframework==3.14.0"],
    python_requires=">=3.10",
    zip_safe=False
)
