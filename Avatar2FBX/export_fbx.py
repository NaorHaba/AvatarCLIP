"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.

"""

import os
import sys
sys.path.append('/path/to/fbxsdk/build/lib/Python37_x64')
sys.path.append(os.path.dirname(__file__))

import torch
import os
import numpy as np
import argparse

from tqdm import tqdm
try:
    import FbxCommon
    from FbxCommon import *
    from fbx import *
except:
    print("Error: module FbxCommon and/or fbx failed to import.\n")

from utils.ply_utils import *
from utils.fbx_utils import *

def convert_ply_to_fbx(mesh_file, save_path, model_dir):
    # ==============================================================================
    # Parse SMPL data
    # ==============================================================================
    print("\n\nParsing ply files...... (may take a while)\n")
    smpl_objects = []

    root_dir = os.path.dirname(os.path.abspath(__file__))
    pose_dir = os.path.join(root_dir, 'poses')

    # Read Triangle Mesh
    ply_mesh = read_ply(mesh_file)
    ply_mesh = simplify_mesh(ply_mesh)

    # get SMPL vertices, triangles, skeletons and blend weights
    # rotate to align with smpl model
    colors = np.asarray(ply_mesh.vertex_colors).astype(np.float32)
    ori_vertices = np.asarray(ply_mesh.vertices).astype(np.float32)
    rot_vertices = np.matmul(
        ori_vertices,
        np.array([[1, 0, 0],
                    [0, 0, 1],
                    [0,-1, 0]], dtype=np.float32)
    )
    triangles = np.asarray(ply_mesh.triangles)

    smpl_model = init_smpl_model(model_dir)
    template_object, pose_rot, beta = load_template_smpl(smpl_model, os.path.join(pose_dir, 'stand_pose.npy'))
    joints = template_object['joints'].squeeze().cpu().numpy()
    # Select first 24 joints
    joints = joints[:24, :]

    nearest_ind = find_nearest_ind(rot_vertices, template_object)
    smpl_blend_weights = smpl_model.lbs_weights
    mesh_blend_weights = torch.gather(smpl_blend_weights, 0, torch.from_numpy(nearest_ind).unsqueeze(-1).repeat(1, smpl_blend_weights.shape[-1]))

    # rotate back to initial orientation
    vertices = ori_vertices
    joints = np.matmul(
        joints,
        np.array([[1, 0, 0],
                    [0, 0,-1],
                    [0, 1, 0]], dtype=np.float32)
    )

    tpose_vertices = inv_lbs(smpl_model, rot_vertices, mesh_blend_weights, pose_rot, beta)
    v_shaped = smpl_model.v_template + blend_shapes(beta, smpl_model.shapedirs)
    tpose_joints = vertices2joints(smpl_model.J_regressor, v_shaped).squeeze().cpu().numpy()

    mesh_blend_weights = mesh_blend_weights.permute(1,0).cpu().numpy()  # reshape from (xxxxx, 24) to (24, xxxxx)

    # Example shape of each smpl_object attributes:
    # - 'vertices': shape(179506, 3)
    # - 'triangles': shape(359004, 3)
    # - 'joints': shape(24, 3)
    # - 'blend_weights': shape(24, 179506)
    # smpl_objects.append({
    #     'vertices': vertices,
    #     'triangles': triangles,
    #     'joints': joints,
    #     'blend_weights': mesh_blend_weights,
    #     'name': ply_name.split('.')[0]
    # })
    smpl_object = {
        'vertices': tpose_vertices * 100,
        'triangles': triangles,
        'joints': tpose_joints * 100,
        'blend_weights': mesh_blend_weights,
        'name': os.path.basename(mesh_file).split('.')[0],
        'colors': colors,
    }

    # ==============================================================================
    # Convert to FBX
    # ==============================================================================

    # Prepare the FBX SDK
    (lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()

    # Create the scene
    lResult = CreateScene(lSdkManager, lScene, smpl_object)

    if lResult == False:
        print(f"\n\nAn error occurred while creating the scene for: {smpl_object['name']}\n")
        lSdkManager.Destroy()
        sys.exit(1)

    lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_EMBEDDED, True)
    lFileFormat = lSdkManager.GetIOPluginRegistry().GetNativeWriterFormat()

    # Save the scene
    lResult = FbxCommon.SaveScene(lSdkManager, lScene, save_path)

    if lResult == False:
        print(f"\n\nAn error occurred while saving the scene for: {smpl_object['name']}\n")
        lSdkManager.Destroy()
        sys.exit(1)
        

    # Destroy all objects created by the FBX SDK
    lSdkManager.Destroy()
    sys.exit(0)


if __name__ == "__main__":

    # ==============================================================================
    # Parse SMPL data
    # ==============================================================================
    print("\n\nParsing ply files...... (may take a while)\n")
    smpl_objects = []

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--mesh_file', type=str, required=True)
    arg_parser.add_argument('--save_path', type=str, required=True)
    arg_parser.add_argument('--model_dir', type=str, required=True)
    args = arg_parser.parse_args()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    pose_dir = os.path.join(root_dir, 'poses')

    mesh_file = args.mesh_file
    save_path = args.save_path
    model_dir = args.model_dir

    # Read Triangle Mesh
    ply_mesh = read_ply(mesh_file)
    ply_mesh = simplify_mesh(ply_mesh)

    # get SMPL vertices, triangles, skeletons and blend weights
    # rotate to align with smpl model
    colors = np.asarray(ply_mesh.vertex_colors).astype(np.float32)
    ori_vertices = np.asarray(ply_mesh.vertices).astype(np.float32)
    rot_vertices = np.matmul(
        ori_vertices,
        np.array([[1, 0, 0],
                    [0, 0, 1],
                    [0,-1, 0]], dtype=np.float32)
    )
    triangles = np.asarray(ply_mesh.triangles)

    smpl_model = init_smpl_model(model_dir)
    template_object, pose_rot, beta = load_template_smpl(smpl_model, os.path.join(pose_dir, 'stand_pose.npy'))
    joints = template_object['joints'].squeeze().cpu().numpy()
    # Select first 24 joints
    joints = joints[:24, :]

    nearest_ind = find_nearest_ind(rot_vertices, template_object)
    smpl_blend_weights = smpl_model.lbs_weights
    mesh_blend_weights = torch.gather(smpl_blend_weights, 0, torch.from_numpy(nearest_ind).unsqueeze(-1).repeat(1, smpl_blend_weights.shape[-1]))

    # rotate back to initial orientation
    vertices = ori_vertices
    joints = np.matmul(
        joints,
        np.array([[1, 0, 0],
                    [0, 0,-1],
                    [0, 1, 0]], dtype=np.float32)
    )

    tpose_vertices = inv_lbs(smpl_model, rot_vertices, mesh_blend_weights, pose_rot, beta)
    v_shaped = smpl_model.v_template + blend_shapes(beta, smpl_model.shapedirs)
    tpose_joints = vertices2joints(smpl_model.J_regressor, v_shaped).squeeze().cpu().numpy()

    mesh_blend_weights = mesh_blend_weights.permute(1,0).cpu().numpy()  # reshape from (xxxxx, 24) to (24, xxxxx)

    # Example shape of each smpl_object attributes:
    # - 'vertices': shape(179506, 3)
    # - 'triangles': shape(359004, 3)
    # - 'joints': shape(24, 3)
    # - 'blend_weights': shape(24, 179506)
    # smpl_objects.append({
    #     'vertices': vertices,
    #     'triangles': triangles,
    #     'joints': joints,
    #     'blend_weights': mesh_blend_weights,
    #     'name': ply_name.split('.')[0]
    # })
    smpl_object = {
        'vertices': tpose_vertices * 100,
        'triangles': triangles,
        'joints': tpose_joints * 100,
        'blend_weights': mesh_blend_weights,
        'name': os.path.basename(mesh_file).split('.')[0],
        'colors': colors,
    }

# ==============================================================================
# Convert to FBX
# ==============================================================================

    # Prepare the FBX SDK
    (lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()

    # Create the scene
    lResult = CreateScene(lSdkManager, lScene, smpl_object)

    if lResult == False:
        print(f"\n\nAn error occurred while creating the scene for: {smpl_object['name']}\n")
        lSdkManager.Destroy()
        sys.exit(1)

    lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_EMBEDDED, True)
    lFileFormat = lSdkManager.GetIOPluginRegistry().GetNativeWriterFormat()

    # Save the scene
    lResult = FbxCommon.SaveScene(lSdkManager, lScene, save_path)

    if lResult == False:
        print(f"\n\nAn error occurred while saving the scene for: {smpl_object['name']}\n")
        lSdkManager.Destroy()
        sys.exit(1)
        

    # Destroy all objects created by the FBX SDK
    lSdkManager.Destroy()
    sys.exit(0)
