import torch
import cudaq
import numpy as np
import matplotlib.pyplot as plt
from src.utils.data_utils import convert_to_greyscale, normalize_greyscale, extract_patches


def run_quantum_kernel_filter(img: torch.Tensor,
                              is_greyscale: bool,
                              stride: int,
                              kernel_size: int,
                              quantum_kernel,
                              zeeman_strength: float,
                              j1: float,
                              j2: float,
                              sample_count: int,): 
    
    # 1 - greyscale if not already
    if not is_greyscale:
        img_grey = convert_to_greyscale(img)
    else:
        img_grey = img

    # 2 - normalize grayscale values to [-1, 1] and convert to radians
    img_grey = normalize_greyscale(img_grey)

    # 3 - extract patches
    patches = extract_patches(img_grey, kernel_size=kernel_size, stride=stride)

    # 4 - set output feature map
    H, W = img_grey.shape
    H_out = (H - kernel_size) // stride + 1
    W_out = (W - kernel_size) // stride + 1
    feature_map = torch.zeros(H_out, W_out)

    # 5 - run QK on each patch
    for idx, patch in enumerate(patches):
        patch_rotations = patch.tolist()

        # Sample obervations
        bitstring_observed_counts = cudaq.sample(quantum_kernel, patch_rotations, j1, j2, zeeman_strength, shots_count=sample_count)
        
        # Map flat index to 2D feature map, keeping only the most frequently observed bitstring converted to its binary representation's number
            # Pseudo-magnetic phases from the 2^n possible bitstrings. Potential to reduce phase space via symmetry arguments.
        i = idx // W_out
        j = idx % W_out
        feature_map[i, j] = int(bitstring_observed_counts.most_probable(), 2) # converts binary bitstring to an integer 

    return feature_map


def show_images_grid(images, rows, cols, font_size=8):
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2))
    axs = axs.flatten()

    for i, ax in enumerate(axs):
        if i < len(images):
            ax.imshow(images[i][-1].numpy(), cmap='viridis')
            ax.axis('off')

            text = f'$J_1$ = {np.round(images[i][0], 3)}\n $J_2$ = {np.round(images[i][1], 3)}\n $B$ = {np.round(images[i][2], 3)}'
            if len(images[i]) > 4:
                text = f'samples = {images[i][3]}\n ' + text
            ax.text(0.95, 0.80, text, fontsize=font_size, ha='right', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.95, boxstyle='round,pad=0.2'))

        else:
            ax.axis('off')

    plt.tight_layout()
    plt.show()