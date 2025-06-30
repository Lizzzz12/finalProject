from setuptools import setup, find_packages

setup(
    name="ecommerce_price_tracker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'selenium',
        'scrapy',
        'pandas',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'price-tracker=main:main',
        ],
    },
)
setup.py
# from setuptools import setup, find_packages
#
# setup(
#     name='your_package_name',
#     version='0.1',
#     packages=find_packages(where='src'),
#     package_dir={'': 'src'},
# )
