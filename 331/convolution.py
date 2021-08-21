from typing import Optional

import numpy as np
from numpy import ndarray


def convolution2D(
        image: np.array, kernel: np.array, padding: Optional[int] = None, stride: int = 1
) -> np.array:
    """Calculate the convolution between the input image and a filter, returning the feature map.

    Args:
        image (np.array): Input image as 2d array with height x width. Supposed to have equal dimensions.
        kernel (np.array): Filter or kernel as 2d array with height x width. Supposed to have equal and odd dimensions.
        padding (Optional[int]): Border around the image with pixels of value 0. If None, defaults to p = (f - 1) / 2.
        stride (int): Step length to move the filter over the image. Defaults to 1.

    Returns:
        np.array: the feature map constructed from the image and the kernel.
    """
    # Parameter validation
    if not (isinstance(image, ndarray) and isinstance(kernel, ndarray)):
        raise TypeError('image and filter must both be supplied as np.array objects')
    if not (len(image.shape) == 2 and len(kernel.shape) == 2):
        raise ValueError('image and filter must both be 2D arrays')
    if not (image.shape[0] == image.shape[1] and kernel.shape[0] == kernel.shape[1]):
        raise ValueError('image and filter must be quadratic sized arrays')
    if not (image.dtype.kind in 'uifc' and kernel.dtype.kind in 'uifc'):
        raise TypeError('image and filter must both contain numeric values')
    if not (kernel.shape[0] % 2 == 1):
        raise ValueError('filter must be of an odd size')
    if image.shape[0] < kernel.shape[0]:
        raise ValueError('image must be larger than filter')
    if padding or padding == 0:
        if not (isinstance(padding, int)):
            raise TypeError('padding must be an integer')
        if padding < 0:
            raise ValueError('padding must be greater or equal to the value zero')
    else:
        # padding not passed, needs a default… half of the filter size
        padding = (kernel.shape[0] - 1) // 2
    if not (isinstance(stride, int)):
        raise TypeError('stride myst be an integer')
    if stride < 1:
        raise ValueError('stride must be greater or equal to the value one')
    # end of validations

    # Perform the convolution
    # work out the size of the output matrix (both dimensions are equal as the input dimensions are equal):
    image_dim = image.shape[0]
    kernel_dim = kernel.shape[0]
    out_dim = int(np.floor((image_dim - kernel_dim + 2 * padding) / stride) + 1)
    out_mat = np.zeros((out_dim, out_dim))

    # Make a working image with padding for the convolution to work with
    working_dim = image_dim + 2 * padding
    if padding > 0:
        working_image = np.zeros((working_dim, working_dim))
        # copy original image into the middle of the working image
        working_image[padding:-padding, padding: -padding] = image
    else:
        working_image = image.copy()

    # loop through the rows and columns of the image to perform the convolution
    for row in range(out_dim):
        # work out the start row of where this output row with begin storing
        working_row_base = row * stride
        for col in range(out_dim):
            # the output value is the dot product of the filter array with a
            # same sized section of the working image corresponding to the
            # appropriate stride value
            working_col_base = col * stride
            working_section = working_image[working_row_base:working_row_base + kernel_dim,
                              working_col_base:working_col_base + kernel_dim]
            out_mat[row, col] = (kernel * working_section).sum()

    return out_mat
