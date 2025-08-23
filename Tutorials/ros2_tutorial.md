## Build Ros2:

Step1: create /src

```shell
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Step2: build package folder

```shell
ros2 pkg create --build-type ament_python my_package --dependencies rclpy
```

Step3: 
Now the folder looks like:

```shell
my_package/
  package.xml
  setup.py
  my_package/
    __init__.py
  resource/
```

put node python file in `my_package/my_package/my_node.py`

Step4:
Modify `setup.py`

```python
data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*config.[pxy][yma]*'))),
        ...
    ],

...

entry_points={
    'console_scripts': [
        'execution_hint = my_package.my_node:main'
    ],
},
```

point colcon to launch/config/... folders

command name to execute the node: execution_hint

package name:my_package

the name in `ros2 pkg create my_package`

file name: my_node

Python file name, my_node.py, without .py 

function name: main

main function in my_node.py

If it said no executable files in the following steps, it should because you are not trying to execute `execution_hint`, but `my_node.py`

Step5:

do 

```shell
cd ~/ros2_ws
colcon build
source install/setup.bash
```

Then start:
```shell
ros2 run my_package execution_hint
```


