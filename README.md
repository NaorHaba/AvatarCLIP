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

finally, to convert the created avatars to a format that can be used in Unity ('fbx' format), we need to install packages 
according to the instructions in the original project (steps 1-3):
https://github.com/hongfz16/AvatarCLIP/tree/main/Avatar2FBX



## Data Preparation

For this section, start by following the instructions in the original project.

Then, .... TODO

## Running the Code

As we mentioned before, this fork provides an interface to run the process of avatar generation. <BR>
To do so, we created a website (running with Streamlit on localhost) that allows the user to control each step of the process. <BR>
To run the website, run the following command:

```bash
python -m streamlit run website/Home.py
```

The website will open in your browser, and you can start generating avatars. 
Usage is pretty straightforward, but we will explain the process in more detail in the following sections.

The website is using a settings file to store the user's preferences. <BR>
The process of generating avatars can be divided into two main parts: <BR>
1. Coarse Shape Generation
2. Shape Sculpting and Texture Generation

Outputs of the first part are necessary for the second part, so the user must run the first part before running the second part. <BR>
Also, due to the nature of the process, we divided the outputs of the model into 2 folders: <BR>
1. `coarse_shape` - contains the coarse shape of the model. <BR>
2. `generated_avatar` - contains the final avatar, after the shape sculpting and texture generation together with the fbx format. <BR>

Each of the steps in the process is logged according to the settings file and the user can view the status of each step in the log. <BR>

According to the nature of the above, the website has the following structure: <BR>

### View Generated Coarse Shape
In this section, the user can view the generated coarse shapes so far. 
For each generated coarse shape we are specifying for each part of the coarse shape generation its status (done/not done): <BR>
1. "OBJ file"
2. "Render folder"
3. "implicit folder"

### View Generated Avatars
In this section, the user can view the generated avatars so far.
For each generated avatar we are specifying for each part of the avatar generation its status (done/not done): <BR>
1. "Texture folder"
2. "FBX file"

### Generate New Coarse Shape
In this section, the user can generate a new coarse shape. <BR>
To do so, the user needs to provide a prompt for the coarse shape generation such as 'a tall person', 'a short person', 'a fat person', etc. <BR>
More examples can be found in `output/coarse_shape`

### Render Coarse Shape
In this section, the user can render the coarse shape that was generated in the previous section. <BR>
The user needs to choose the coarse shape that was generated in the previous section for which he wants to render the avatar. <BR>

### Initialize Implicit Avatar
In this section, the user can initialize the implicit avatar that was generated in the previous section. <BR>
This is in fact a pretraining step for the shape sculpting and texture generation. 
The model which will be used for the shape sculpting and texture generation is initialized with the implicit avatar.

This step is dependent on GPU resources. In order to run this step, the user needs to have a GPU installed on his machine. 
We are providing 2 options for the size of the model: small and large, which the user can choose from. <BR>
The small model is faster to train and requires less resources, but the results are not as good as the large model. <BR>

This step can take a long time so we are running it in the background and send the user an email (if he provided his email) when it is done.
Please make sure that the machine will not be shut down before the process is done.
If the process dies for some reason, the user can run it again and continue from where it stopped. <BR>

NOTICE! <BR> 
This step is not necessary for the user to run, but it is recommended to run it. If the user chooses so, he can use a default model instead. <BR>

### Generate Texture
In this section, the user can generate the texture of the avatar that was generated in the previous section. <BR>
The user needs to choose the avatar that was generated in the previous section for which he wants to generate the texture. <BR>
Also, the user needs to provide a prompt for the texture generation such as 'a basketball player', 'a circus performer', 'a sumo wrestler', etc. <BR>
More examples can be found in `output/generated_avatar`

This step is also dependent on GPU resources. The user should act according to the previous step. <BR>

This step can also take a long time, so we operate the same as in the previous step. <BR>

### Generate FBX
In this section, the user can generate the fbx file of the avatar that was generated in the previous section. <BR>
The user needs to choose the avatar that was generated in the previous section for which he wants to generate the fbx file. <BR>


### Settings
In this section, the user can change the settings of the website. <BR>
The settings are stored in the file `website/settings_files/settings.yaml`. <BR>
We recommend not to change the settings unless you know what you are doing. <BR>

Also this is the place where the user can provide his email address. <BR>


### Run From File
In this section, the user can run the process of avatar generation (or multiple avatars) from a  file. <BR>
Example is provided in the website itself. <BR>


## Running the Code - Advanced
We provide a simple yet useful interface to run the process of avatar generation. 
However, this interface is limited in some ways that some users might want to overcome. <BR>
For a more advanced usage, a user can refer to the original project, and follow the instructions there. <BR>
https://github.com/hongfz16/AvatarCLIP


## Acknowledgements
This project is supported through the AVR lab at the Israel Institute of Technology - The Technion. <BR>
We would like to thank the faculty members, Boaz Sternfeld and Yaron Honen, for their support and guidance. <BR>
