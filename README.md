# Magnetic frustration as a guide to quantum algorithm design

One of the potential benefits of quantum machine learning (QML) is the ability to leverage the exponentially large Hilbert space of quantum systems to represent and learn complex patterns from data that may be classically intractable. However, QML algorithms can also suffer from *barren plateaus* (regions in the optimization landscape wherein the gradient vanishes), making learning and training extremely difficult and heavily dependent on parameter initialization. The goal of this project is to utilize concepts from condensed matter physics, specifically *magnetic frustration*, as a naive conceptual guide to circumvent this pitfall and create expressive quantum circuits and algorithms. 

The overall idea is to pre-place a quantum kernel proximate to multiple quantum phase boundaries, and then let minor perturbations from data inputs to swap between neighboring phases. These phase crossings are then the fundamental source of learning in the machine learning task.

As an initial test, this project focuses on image augmentation and convolutions to extract classical image features by adapting the principles behind the *frustrated J1-J2 square-lattice Hamiltonian* to convolutional kernels.

## Objective
Create a series of quantum kernels that convolve an image to detect features as a typical classical CNN convolutional layer would, but with parameters conceptually defined via magnetically-frustrated Hamiltonians.

## Methodology
- Design a series of quantum kernels with varying entanglements & (controlled-)rotation operations that *mimic* frustration parameters.
- Inputs: image pixel patches (2x2, 3x3, and eventually larger)
- Kernel: sweeps across image patches via *stride* to convert image features to `magnetic texturings` and `phase boundaries` to improve an image classification task
- Output: in early NISQ, the varying `frustrated kernels` can be used as image *augmentations*, with the longer-term goals of:
    1) weighting these kernels by learnable parameters in a typical CNN setup (early-to-mid NISQ)
    2) entangling multiple neighboring kernels simultaneously (mid NISQ)
    3) directly linking to quantum fully-connected layers, such as the one present in the `hqnn_image_classification` project [https://github.com/mitchellmb/hqnn_image_classification] (late NISQ) 

## Project structure
This project leverages the `hqnn_image_classification` data from TensorFlow datasets, and augments these images with the frustration-based quantum convolutional kernels coded in CUDA-Q.

## Future outlook
The design principles of these frustrated quantum kernels can be easily adapted to other general quantum algorithm tasks, not just image classifications, as long as the underlying quantum circuit is pre-placed in the Hilbert space proximate to one-or-more phase boundaries.