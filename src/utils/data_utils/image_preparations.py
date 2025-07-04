import torch
import numpy as np


def extract_patches(gray_image: torch.Tensor, kernel_size=2, stride=1): 
    # image patch extraction, overlap set by stride (pixel width)
    patches = gray_image.unfold(0, kernel_size, stride).unfold(1, kernel_size, stride)
    patches = patches.contiguous().view(-1, kernel_size * kernel_size)
    return patches


def normalize_greyscale(img: torch.Tensor):
    # normalization for greyscale images & conversion to radians for rotations with CUDA-Q
    img_min = img.min()
    img_max = img.max()
    img_norm = 2 * (img - img_min) / (img_max - img_min) - 1
    return torch.arcsin(img_norm)


def convert_to_greyscale(img):
    # greyscale conversion via standard luminance weights from RGB
    # Y = 0.299 * R + 0.587 * G + 0.114 * B
    return 0.299*img[0] + 0.587*img[1] + 0.114*img[2]


def convert_torch_for_plotting(torch_image, normalized=False):
    # converts torch tensor back to numpy to use with plt.imshow()
    if normalized:
        image = torch_image.permute(1,2,0).numpy()
        rescaled = image*255
        return rescaled.astype(np.uint8)
    
    return torch_image.permute(1,2,0).numpy().astype(np.uint8)