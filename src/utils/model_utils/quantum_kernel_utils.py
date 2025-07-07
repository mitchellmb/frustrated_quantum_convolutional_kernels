import torch
import cudaq
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from src.utils.data_utils.image_preparations import convert_to_greyscale, normalize_greyscale, extract_patches


def run_quantum_kernel_filter(img: torch.Tensor, is_greyscale: bool, stride: int, kernel_size: int, quantum_kernel, 
                              zeeman_strength: float, j1: float, j2: float, sample_count: int,): 
    
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


def dummy_kernel_run(quantum_kernel, zeeman_strength: float, j1: float, j2: float, sample_count: int,):
    # Runs the kernel with given guiding Hamiltonian parameters and a blank image patch

    dummy_patch = np.array([0.,0.,0.,0.])
    bitstring_observed_counts = cudaq.sample(quantum_kernel, dummy_patch, j1, j2, zeeman_strength, shots_count=sample_count)

    return int(bitstring_observed_counts.most_probable(), 2)


def show_images_grid(images, rows, cols, save_path, font_size=8, high_dpi=300, img_downscale=2):
    # Create figure and plot with high DPI for saving
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2), dpi=high_dpi)
    axs = axs.flatten()

    for i, ax in enumerate(axs):
        if i < len(images):
            ax.imshow(images[i][-1].numpy(), cmap='viridis')
            ax.axis('off')

            text = f'$J_1$ = {np.round(images[i][0], 3)}\n $J_2$ = {np.round(images[i][1], 3)}\n $B$ = {np.round(images[i][2], 3)}'
            if len(images[i]) > 4:
                text = f'samples = {images[i][3]}\n ' + text
            ax.text(0.95, 0.80, text, fontsize=font_size, ha='right', va='bottom', transform=ax.transAxes, 
                    bbox=dict(facecolor='white', alpha=0.95, boxstyle='round,pad=0.2'))
        else:
            ax.axis('off')

    plt.tight_layout()
    
    # Save the high-DPI figure to disk
    plt.savefig(save_path, dpi=high_dpi)
    plt.close(fig)

    # Reload the saved image with low DPI for display in Jupyter notebook
    img = Image.open(save_path)
    img = img.convert('RGB')
    img.thumbnail((img.width // img_downscale, img.height // img_downscale))
    img.show()


def plot_individual_phase_diagram(ax, j1_j2_result_list, zeeman_value, font_size=12):
    # Sets a scatter plot for one B-value phase diagram

    j1, j2, val = zip(*j1_j2_result_list)
    
    scatter = ax.scatter(j1, j2, c=val, cmap='viridis', s=10, edgecolor=None, vmin=0, vmax=15)

    ax.set_xlabel('$J_1$', fontsize=font_size)
    ax.set_ylabel('$J_2$', fontsize=font_size)
    ax.set_title(f'$B = {zeeman_value:.3f}$', fontsize=font_size)
    ax.grid(True)
    
    return scatter


def plot_all_phase_diagrams(phase_diagrams_list, rows, cols, save_path, 
                            fig_x=15, fig_y=8, font_size=12, high_dpi=300, img_downscale=2):
    # Plots combined scatter plots for varying B-values across J1-J2 phase diagrams

    fig, axes = plt.subplots(rows, cols, figsize=(fig_x, fig_y), constrained_layout=True)
    axes = axes.flatten()

    last_scatter = None
    for ax, diagram in zip(axes, phase_diagrams_list):

        last_scatter = plot_individual_phase_diagram(ax=ax, j1_j2_result_list=diagram[1], 
                                                     zeeman_value=diagram[0], font_size=font_size)

    cbar = fig.colorbar(last_scatter, ax=axes, ticks=np.arange(0, 16), orientation='vertical', fraction=0.02, pad=0.04)
    cbar.set_label('Bitstring')

    # Save high-DPI & display low-DPI
    plt.savefig(save_path, dpi=high_dpi)
    plt.close(fig)

    img = Image.open(save_path)
    img = img.convert('RGB')
    img.thumbnail((img.width // img_downscale, img.height // img_downscale))
    img.show()