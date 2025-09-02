import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mecanum_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ntdev204',
    maintainer_email='ntdev204@todo.todo',
    description='Keyboard teleoperation for Mecanum robot',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_keyboard = mecanum_teleop.teleop_keyboard:main',
            'teleop_joy = mecanum_teleop.teleop_joy:main',
        ],
    },
)
