from setuptools import setup,find_packages
packages=find_packages()
packages.remove('common_utils')
print(packages)
setup(
      author="chandim",
      author_email="chandimsett@gmail.com",
      packages=packages,
      include_package_data=True,
      name='ml_automation',
      version='0.0.2',
      description='ml_automation',
)