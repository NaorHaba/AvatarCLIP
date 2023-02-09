<div align="center">

<h1>AVR-Lab Project About:
"AvatarCLIP: Zero-Shot Text-Driven Generation and Animation of 3D Avatars"</h1>

</div>

This repository is forked from the original [AvatarCLIP](https://github.com/hongfz16/AvatarCLIP) repository.
In this fork, we aim to provide more detailed instructions to run parts of the project, as well as a more user-friendly interface to generate avatars.

Currently, we only provide instructions to run the avatar generation part of the project as no instructions are yet available to convert the created animations to an FBX file.

We highly recommend you to read the original README file for more information about the project.

## Installation

In the following section we will explain how to install the project on your local machine. 
We will assume that you are using a Linux machine, but the installation should be similar on other operating systems.

As some dependencies of the project require configuring system related resources (which are not python packages), 
we use conda to manage the environment as it also allows to install system dependencies.

### 1. Create a Conda Environment

First, we need to create a conda environment. We specify the python version to be 3.7, according to the requirements of the project.
    
```bash
conda create -n AvatarCLIP python=3.7
conda activate AvatarCLIP
```

### 2. Install Specific Versions of GCC and G++

(Only required if your system uses GCC and G++ versions higher than 8.0)

The project uses a python package named `neural_renderer` which requires specific versions of GCC and G++.
When running this package installation, it is stated that versions later than 8 are not supported for GCC and G++.
Therefore, we need to install specific versions of GCC and G++ - we will use version 7.5.0.

First, to view the current version of GCC and G++ installed on your system, run the following commands:

```bash
gcc --version
g++ --version
```

The output should be similar to the following:

```bash
gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
Copyright (C) 2019 Free Software Foundation, Inc.
```

```bash
g++ (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
Copyright (C) 2019 Free Software Foundation, Inc.
```

If the versions are higher than 8.0, you will need to install the supported versions of GCC and G++.
To do so, run the following commands:

```bash
conda install gcc_linux-64=7.5.0
conda install gxx_linux-64=7.5.0
```

Then, link the new versions of GCC and G++ to your system:

```bash
cd /home/your_username/miniconda3/envs/AvatarCLIP/bin
ln -s /home/your_username/miniconda3/envs/AvatarCLIP/bin/x86_64-conda_cos6-linux-gnu-gcc gcc
ln -s /home/your_username/miniconda3/envs/AvatarCLIP/bin/x86_64-conda_cos6-linux-gnu-g++ g++
```


cd /home/eitan.g/miniconda3/envs/AvatarCLIP/bin
ln -s /home/eitan.g/miniconda3/envs/AvatarCLIP/bin/x86_64-conda_cos6-linux-gnu-gcc gcc
ln -s /home/eitan.g/miniconda3/envs/AvatarCLIP/bin/x86_64-conda_cos6-linux-gnu-g++ g++

To verify that the new versions of GCC and G++ are installed, first deactivate the conda environment and then reactivate it:

```bash
conda deactivate
conda activate AvatarCLIP
```

Then, run the following commands:

```bash
gcc --version
g++ --version
```

The output should be similar to the following:

```bash
gcc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0
Copyright (C) 2018 Free Software Foundation, Inc.
```

```bash
g++ (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0
Copyright (C) 2018 Free Software Foundation, Inc.
```


### 3. Install Python Packages

The original project suggests to install some packages using `conda` and others using `pip`.
It is usually recommended to use only one package manager, but because some of them are only available on `conda` and others on `pip`,
we have to use both.

To maintain stability in the environment, we will install all the packages using `conda` and then install the remaining packages using `pip`.

First, install the packages using `conda` according to the following order (changing the order might cause dependency errors and lead to the infamous [dependency hell](https://en.wikipedia.org/wiki/Dependency_hell)):

```bash
conda install -c menpo osmesa
conda install pytorch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0 cudatoolkit=10.1 -c pytorch
```

Next, clone the project repository:

```bash
git clone https://github.com/hongfz16/AvatarCLIP.git
cd AvatarCLIP
```

For the next part, we will use the `requirements.txt` file provided in the project repository to install the remaining packages.
Please notice that `neural_renderer` is trying to access GPU resources while installing, so you must have a GPU installed on your machine.
If you are using a virtual server (like Lambda on Technion), you can access a GPU node buy running the following command:

```bash
srun --gres=gpu:1 --pty bash
```

Then, install the remaining packages using `pip` from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

Notice, after installing the packages using `pip` the environment might be broken, but running the code is possible, so we leave it as is.
This problem however will affect running the avatar animation part of the project (which is not yet supported in this fork).
We couldn't find a solution to this problem, but we are open to suggestions.

Moreover, due to the broken environment we need to change some files in the `neural_renderer` package.
In this package, sk-image is used to load and save images, but the package is not installed in the environment.
Instead, we use `PIL` and `numpy` to load and save images.

To do so, open the file `neural_renderer/load_obj.py` and change the following lines:

line 6:
```python
from skimage.io import imread
```

to

```python
from PIL.Image import open as imread
```

and

line 89:
```python
image = imread(filename_texture).astype(np.float32) / 255.
```

to

```python
image = np.asarray(imread(filename_texture), dtype=np.float32) / 255.
```

Then, open the file `neural_renderer/save_obj.py` and change the following lines:

line 5:
```python
from skimage.io import imsave
```

to

```python
from numpy import save as imsave
```

also as stated in the original project, we need to add the following three lines to neural_renderer/perspective.py after line 19.

```python
x[z<=0] = 0
y[z<=0] = 0
z[z<=0] = 0
```

## Data Preparation

For this section, start by following the instructions in the original project.

Then, .... TODO

## Running the Code

### Avatar Generation - Coarse Shape Generation

Folder `AvatarGen/ShapeGen` contains codes for this part. Run the follow command to generate the coarse shape corresponding to the shape description 'a strong man'. We recommend to use the prompt augmentation 'a 3d rendering of xxx in unreal engine' for better results. The generated coarse body mesh will be stored under `AvatarGen/ShapeGen/output/coarse_shape`.

```bash
python main.py --target_txt 'a 3d rendering of a strong man in unreal engine'
```

Then we need to render the mesh for initialization of the implicit avatar representation. Use the following command for rendering.

```bash
python render.py --coarse_shape_obj output/coarse_shape/a_3d_rendering_of_a_strong_man_in_unreal_engine.obj --output_folder ${RENDER_FOLDER}
```

### Avatar Generation - Shape Sculpting and Texture Generation

Note that all the codes are tested on NVIDIA V100 (32GB memory). Therefore, in order to run on GPUs with lower memory, please try to scale down the network or tune down `max_ray_num` in the config files. You can refer to `confs/examples_small/example.conf` or our [colab demo](https://colab.research.google.com/drive/1dfaecX7xF3nP6fyXc8XBljV5QY1lc1TR?usp=sharing) for a scale-down version of AvatarCLIP.

Folder `AvatarGen/AppearanceGen` contains codes for this part. We provide data, pretrained model and scripts to perform shape sculpting and texture generation on a zero-beta body (mean shape defined by SMPL). We provide many example scripts under `AvatarGen/AppearanceGen/confs/examples`. For example, if we want to generate 'Abraham Lincoln', which is defined in the config file `confs/examples/abrahamlincoln.conf`, use the following command.

```bash
python main.py --mode train_clip --conf confs/examples/abrahamlincoln.conf
```

Results will be stored in `AvatarCLIP/AvatarGen/AppearanceGen/exp/smpl/examples/abrahamlincoln`.

If you wish to perform shape sculpting and texture generation on the previously generated coarse shape. We also provide example config files in `confs/base_models/astrongman.conf` `confs/astrongman/*.conf`. Two steps of optimization are required as follows.

```bash
# Initilization of the implicit avatar
python main.py --mode train --conf confs/base_models/astrongman.conf
# Shape sculpting and texture generation on the initialized implicit avatar
python main.py --mode train_clip --conf confs/astrongman/hulk.conf
```

### Marching Cube

To extract meshes from the generated implicit avatar, one may use the following command.

```bash
python main.py --mode validate_mesh --conf confs/examples/abrahamlincoln.conf
```

The final high resolution mesh will be stored as `AvatarCLIP/AvatarGen/AppearanceGen/exp/smpl/examples/abrahamlincoln/meshes/00030000.ply`

## Convert Avatar to FBX Format

For the convenience of using the generated avatar with modern graphics pipeline, we also provide scripts to rig the avatar and convert to FBX format. See the instructions [here](./Avatar2FBX/README.md).

### Make your own configure

Each configuration contains three independent parts: general setting, pose generator, and motion generator.

```text
# General Setting
general {
    # describe the results path
    base_exp_dir = ./exp/motion_ablation/motion_optimizer/raise_arms

    # if you only want to generate poses, then you can set "mode = pose".
    mode = motion

    # define your prompt. We highly recommend using the format "a rendered 3d man is xxx"
    text = a rendered 3d man is raising both arms
}

# Pose Generator
pose_generator {
    type = VPoserCodebook
    # you can change the number of candidate poses by setting "topk = 10"
    # for PoseOptimizer and VPoserOptimizer, you can further define the number of iterations and the optimizer type
}

# Motion Generator
# if "mode = pose", you can ignore this part
motion_generator {
    type = MotionOptimizer
    # you can further modify the coefficient of each loss. 
    # for example, if you find the generated motion is very intensive, you can reduce the coefficient of delta loss.
}


```