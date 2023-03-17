# AVR-Lab Research Project
## AvatarCLIP - Zero-Shot Text-Driven Generation and Animation of 3D Avatars
#### Naor Haba & Eitan Greenberg


## Abstract
In this project, we present our work during a research project under the AVR-Lab at the Technion.
The project was focused on the development of a system that can generate and animate 3D avatars from text descriptions.
Specifically, we followed the paper of AvatarCLIP, a novel work by [[Fangzhou Hong et al. 2022]](#AvatarCLIP) that uses a conditional variational autoencoder to generate 3D avatars from text descriptions.
Our aim was to understand the paper and reproduce the results, while also trying to integrate the generated avatars into a Unity scene.
Our work concludes with a Unity scene integrating the generated avatars, and a website built over the original paper's code that allows the user to use this technology in a more user-friendly manner.

## Introduction
Recently, there has been a lot of interest in the field of text-driven content generation.
This includes the generation of texts, images, and recently, 3D avatars and animations.
These capabilities enable the user to generate content based on a text description, without the need to create the content manually.
Specifically, in 3D content generation, this enables the creation of realistic and expressive avatars, bringing a new level of interactivity to virtual environments, gaming, social media, and other applications.

The generation of 3D avatars has been a tedious and time-consuming task that requires expertise in both 3D modeling and animation.
Zero-shot text-driven generation and animation of 3D avatars is an emerging field of research that has the potential to revolutionize the way we interact with virtual environments. 
With this technology, users can generate and animate 3D avatars simply by providing text input, without the need for any specialized skills or knowledge,
thus shortening the time and effort required to create 3D content.

Taking these reasons into account, we took on the task of understanding the paper of AvatarCLIP, which uses the powerful
vision-language model CLIP for supervising neural human generation, in terms of 3D geometry, texture and animation.
Following this paper we provide an easy-to-use implementation of the technology, and show its capabilities in a Unity scene.
We hope that this work will help bridging the gap between research and application, and will enable the use of this technology to create new and exciting applications.

## Understanding AvatarCLIP
The paper proposes a framework for generating and animating 3D avatars using natural language descriptions. 
The authors leverage the powerful vision-language model CLIP to supervise the generation of 3D geometry, texture, and animation. 
The proposed framework involves using a shape VAE network to initialize 3D human geometry generation, 
volume rendering to facilitate geometry sculpting and texture generation, and a CLIP-guided reference-based motion synthesis 
method for animation. The authors conduct extensive experiments that demonstrate the effectiveness and generalizability of 
AvatarCLIP on a wide range of avatars, achieving superior zero-shot capability for generating unseen 3D avatars with novel animations 
as we will show in the Unity scene.
The paper also highlights the challenges of static avatar generation and motion synthesis using CLIP, and proposes solutions 
such as using neural rendering for generating implicit 3D avatars and clustering diverse poses for candidate poses that serve 
as clues for motion synthesis.

Overall, to generate and animate 3D avatars, the proposed framework consists of the following steps:

- Driven by natural language descriptions, a shape VAE network is used to initialize 3D human geometry generation.
- Based on the generated 3D human shapes, a volume rendering model is utilized to further facilitate geometry sculpting and texture generation.
- By leveraging the priors learned in the motion VAE, a CLIP-guided reference-based motion synthesis method is proposed for the animation of the generated 3D avatar. 
  - In the first stage of motion synthesis, a code-book consisting of diverse poses is created by clustering, and poses that match motion descriptions are selected by CLIP from the code-book.
  - In the second stage of motion synthesis, a motion VAE is utilized to learn motion priors, which facilitates the reference-guided motion synthesis.

## Using AvatarCLIP
Together with the paper, the authors released a code repository that allows the user to generate and animate 3D avatars 
from text descriptions according to the paper's method.
However, trying to follow the paper's instructions using the designated resources we received was hard and resulted in many errors.

First, the repository's instructions require the user to install some packages but as it turns out, these 
instructions are not compatible with the server we were using.
This was a major issue, hindering our progress massively as we needed to use the help of the server's administrator to install the packages.
Second, apparently, the installation instructions are not complete, as we had to install some additional packages to be able to run the code.
This led to more errors, as some of the added packages were not compatible with the other packages.

To overcome these issues, we had to alter the original and package's code in order to make it work, which eventually left us with the ability 
to only generate 3D avatars and not animate them (the environment was not compatible with the animation part of the code).
We decided not to waste more efforts on this issue as we also noticed the code is not supporting converting the generated animations to an FBX format yet
(supporting only converting the avatars to FBX format without the animation).
Finally, whilst not an issue with the server or the code, the GPU resources we were given were not as the paper's authors used and recommended.
Trying to generate avatars with the same parameters as the paper's authors used resulted in a memory error, and we had to reduce the parameters in order to generate the avatars.
After reducing the parameters, we were able to generate the avatars, but the quality was poor and the avatars were not as realistic as the ones in the paper.

Despite all these issues, we were able to run the complete code steps to generate a single 3D avatar which had a poor quality but still resembled the description.
At this point in time, we decided to move on to build an easy interface through a website, 
planning to come back to generating more avatars in an easy manner and to create multiple avatars at once.

However, as with all good plans, unforeseen events can always show up, and as we were nearing the end of building the interface,
the Technion was hacked, and we lost access to the server until the end of the semester. 
This meant that we were unable to continue our work which affected both our ability to check finish the website and check that the full pipeline works,
and our ability to generate more avatars. So eventually we were left with a working interface at the most part, and with only one generated avatar.
However, we still had many avatars from the paper's authors that we could use in our Unity scene.

## Interface For AvatarCLIP
The interface we built is based on the original code repository, and allows the user to generate 3D avatars from text descriptions.
It allows to user a basic usage of the technology, and to generate avatars in an easy manner and in the most common (and recommended by the authors) way.
A complete description of the interface can be found in the README file of the repository of our project.

## AvatarCLIP in Unity
We decided to use Unity to show the generated avatars in a 3D environment, and to allow the user to interact with them.
The scene we created consists of a city environment, with a few buildings and a street, and multiple generated avatars.
The avatars are placed in the scene in a way that they are standing or doing some activity in the street and the user can inertact with them by coming close to them.
The user can also move around the scene and look at the avatars from different angles.
We decided to use the avatars generated by the paper's authors, as we were unable to generate more avatars due to the issues we faced.
The avatars were divided into three groups: General, Fictional and Celebrity, and placed them in the scene accordingly under a floating sign.
Because of the lack of support for converting the generated animations to an FBX format, we decided to use existing animations from [Mixamo](#Mixamo).
By uploading the avatar to mixamo and downloading an animated version of it in FBX format, we were able to use the animations in Unity.
To enable the textures to be displayed correctly in Unity, we had to select the meshNode object of each avatar and change the material of the Skinned Mesh Renderer component to DefaultMateriallVertexColorShader.

The Scene from above:<br>
![All Scene](https://github.com/NaorHaba/AvatarCLIP/blob/main/demo/All%20Scene%20View.gif)
Gameplay View:<br>
![Gameplay View](https://github.com/NaorHaba/AvatarCLIP/blob/main/demo/Gameplay%20View.gif)

## Conclusion
Our research project focused on reproducing the results of the AvatarCLIP paper, which presents a system for generating and animating 3D avatars from text descriptions using a conditional variational autoencoder.
Throughout our project, we successfully integrated the generated avatars into a Unity scene and built a user-friendly website over the original paper's code, allowing for easier access to this technology.

Despite the challenges we faced throughout the project, we are satisfied with the outcome and proud of what we have achieved. 
Our efforts have contributed towards bridging the gap between research and application, 
and we hope that our work will inspire new and exciting applications of this technology. 
Throughout the project, we learned a lot about the field of text-driven content generation and 3D avatar creation, 
which has enriched our knowledge and understanding of this exciting area of research. 
Overall, we feel that our work has made a valuable contribution to the field 
and we look forward to seeing the future developments and advancements in this area.

## References
<a name="AvatarCLIP">[1] [AvatarCLIP](https://github.com/hongfz16/AvatarCLIP): Zero-Shot Text-Driven Generation and Animation of 3D Avatars</a><br>
[2] [CLIP](https://github.com/OpenAI/CLIP): Connecting Text and Images<br>
<a name="Mixamo">[3] [Mixamo](https://www.mixamo.com/#/): Animate 3D characters for games, film, and more.</a>
