from setuptools import setup

package_name = 'mecanum_robot_keyboard'

setup(
    name=package_name,
    version='2.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mecanum',
    maintainer_email='mecanum@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mecanum_keyboard = mecanum_robot_keyboard.mecanum_keyboard:main',
        ],
    },
)
