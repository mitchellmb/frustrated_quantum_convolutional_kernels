# Magnetic frustration as a guide to quantum kernel design

One of the potential benefits of quantum machine learning (QML) is the ability to leverage the exponentially large Hilbert space of quantum systems to represent and learn complex patterns from data that may be classically intractable. However, QML algorithms can also suffer from **barren plateaus** (regions in the optimization landscape wherein the gradient vanishes), making learning and training extremely difficult and heavily dependent on parameter initialization. 

The goal of this project is to utilize concepts from condensed matter physics, specifically **magnetic frustration**, as a naive conceptual guide to circumvent this pitfall and create expressive quantum circuits and algorithms. An introduction to magnetic frustration can be found here: [https://www.nature.com/articles/nature08917].

The overall idea is to pre-place a quantum kernel proximate to multiple quantum phase boundaries, and then let minor perturbations from data inputs to swap between neighboring competitive phases (i.e., bitstrings). These phase crossings are then the initiation point for learning in the follow-up machine learning task.


## Objective
Create `frustrated quantum kernels` with **limited qubits and circuit depth** that convolve an image to detect features as a typical classical CNN convolutional layer would, but with parameters conceptually defined via a magnetically-frustrated Hamiltonian.

As an initial test, this project focuses on image augmentation and convolutions to extract classical image features by adapting the principles behind the `Frustrated J1-J2 square-lattice Hamiltonian` to convolutional kernels. 
- **Parameter competition** between $J_1$ & $J_2$ (exchange interactions), $B$ (external magnetic field), and the number of samples is the source of frustration.
- An optimal balance between these competing parameters (encoded as rotations) places a 2x2 quantum convolutional kernel near quantum phase boundaries.

![frustrated_lattice_diagram](https://github.com/user-attachments/assets/72f6bc51-50da-45a6-9403-04c307f09d8f)

## Methodology
- Design a series of quantum kernels (coded in **CUDA-Q**) with varying entanglements & controlled-rotation operations that **mimic** frustration parameters.
- Inputs: image pixel patches (2x2, 3x3, and eventually larger)
- Kernel: sweeps across image patches via *stride* to convert image features to `magnetic textures` and `magnetic phase boundaries / domain walls` to improve an image classification task
- Output: in early NISQ, the varying kernels can be used as image **augmentations**, with the longer-term goals of:
    1) Weighting these kernels by learnable parameters in a typical CNN setup (early-to-mid NISQ)
    2) Entangling multiple neighboring kernels simultaneously (mid NISQ)
    3) Directly linking to quantum fully-connected layers (late NISQ) 
          - E.g., one present in the `hqnn_image_classification` project [https://github.com/mitchellmb/hqnn_image_classification]
    4) Further perturbing the quantum representation of data via magnetically-inspired excitations (e.g., magnons & other quasiparticles)

## Project structure
1) Images:
    - The notebook in this project use images from the `hqnn_image_classification` project, originating from TensorFlow datasets.
    - Any greyscale or RGB image can be used, but note that with increasing image resoltuion computation times increase.
2) Frustrated kernels:
    - 2x2 and 3x3 example kernels are in `./src/quantum_kernels/`
    - The 3x3 kernel effectively contains four `qk_2x2_v2.py` kernels.
        - Additional exchange interactions (e.g., $J_1-J_2-J_3$) could be added here.
3) Example use:
    - `leaf_image_quantum_kernel_augmentation.ipynb` contains details on the derivation & interpretations of a 2x2 frustrated kernel and applies the kernel in `qk_2x2_v2.py` to a specific plant leaf image.
    - High-resolution filtered image examples from the notebook are stored in `./data/`


## Future outlook
1) The design principles of these frustrated quantum kernels can be easily adapted to other general quantum algorithm tasks, not just image classifications, as long as the underlying quantum circuit is pre-placed in the Hilbert space proximate to **one-or-more phase boundaries**.
    - E.g., could be naturally used in generic `quantum kernel methods` (reference: [https://www.nature.com/articles/s41467-024-49287-w])
3) Individual frustrated kernels can combine to increase quantum entanglement of the data or problem, but will require more qubits & circuit depth.
    - By doing so, an initial **product-state-like** system becomes a **fully entangled quantum state** that cannot be decomposed back into a product state.
    - This additional entanglement enhances the **quantum representation** of the encoded data, potentially revealing new **quantum-only features**.
    - I.e., frustrated kernels are product-like building blocks that, when entangled together, evolve into a fully quantum state with richer, more complex data representations.
    - Creates a simple way to scale frustrated kernels as the NISQ era progresses.


## Technologies
- [CUDA-Q](https://developer.nvidia.com/cuda-quantum) - Quantum SDK implementation.
- [TensorFlow](https://www.tensorflow.org/datasets) - Source of plant leaf images. plant_leaves - 4500 healthy/unhealthy leaves, 22 species/health categories
ImageCLEF 2013 plant task dataset.
- Python 3.8+


## Citation
If you use this software or idea in your research, please cite it with the link on the side of the project or as follows:

```bibtex
@software{Mitchell_Bordelon_Frustrated_quantum_convolutional,
    author = {{Mitchell Bordelon}},
    license = {MIT},
    title = {{Frustrated quantum convolutional kernels}},
    url = {https://github.com/mitchellmb/frustrated_quantum_convolutional_kernels},
    version = {master}
}
