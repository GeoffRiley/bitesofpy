import numpy as np
import pytest

from convolution import convolution2D

IMAGE_1x1 = np.array([[1]])
IMAGE_3x3 = np.random.rand(3, 3)
IMAGE_9x9 = np.random.rand(9, 9)
IMAGE_256x256 = np.random.rand(256, 256)

IMAGE_5x5_OUTER_SQUARE = np.array(
    [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
)
IMAGE_5x5_INNER_SQUARE = np.array(
    [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
)
IMAGE_5x5_SQUARES = np.array(
    [
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
    ]
)

KERNEL_1x1 = np.array([[1]])
KERNEL_3x3_SHARPEN = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
KERNEL_3x3_BLUR = np.ones((3, 3)) * 1 / 9
KERNEL_3x3_HORIZONTAL_EDGE = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
KERNEL_3x3_VERTICAL_EDGE = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
KERNEL_5x5 = np.random.rand(5, 5)
KERNEL_5x5_ONES = np.diag(np.ones(5))


@pytest.mark.parametrize(
    "image, kernel, padding, stride, feature_map_size",
    [
        (IMAGE_1x1, KERNEL_1x1, None, 1, (1, 1)),
        (IMAGE_3x3, KERNEL_3x3_SHARPEN, 0, 1, (1, 1)),
        (IMAGE_3x3, KERNEL_3x3_SHARPEN, None, 1, (3, 3)),
        (IMAGE_9x9, KERNEL_3x3_SHARPEN, 0, 1, (7, 7)),
        (IMAGE_9x9, KERNEL_3x3_SHARPEN, None, 1, (9, 9)),
        (IMAGE_9x9, KERNEL_3x3_SHARPEN, 0, 2, (4, 4)),
        (IMAGE_9x9, KERNEL_3x3_SHARPEN, None, 2, (5, 5)),
        (IMAGE_9x9, KERNEL_3x3_SHARPEN, 0, 3, (3, 3)),
        (IMAGE_9x9, KERNEL_3x3_SHARPEN, 2, 3, (4, 4)),
        (IMAGE_256x256, KERNEL_5x5, None, 3, (86, 86)),
    ],
    ids=[
        "image and kernel of size 1x1",
        "image and kernel of size 3x3 with no padding",
        "image and kernel of size 3x3 with default padding",
        "image of size 9x9 and kernel of size 3x3 with no padding",
        "image of size 9x9 and kernel of size 3x3 with default padding",
        "image of size 9x9 and kernel of size 3x3 with no padding and stride 2",
        "image of size 9x9 and kernel of size 3x3 with default padding and stride 2",
        "image of size 9x9 and kernel of size 3x3 with no padding and stride 3",
        "image of size 9x9 and kernel of size 3x3 with padding 2 and stride 3",
        "image of size 256x256 and kernel of size 5x5 with default padding and stride 3",
    ],
)
def test_feature_map_dimension(image, kernel, padding, stride, feature_map_size):
    feature_map = convolution2D(image, kernel, padding, stride)
    np.testing.assert_array_equal(feature_map.shape, feature_map_size)


@pytest.mark.parametrize(
    "image, kernel, padding, stride, feature_map",
    [
        (IMAGE_1x1, KERNEL_1x1, None, 1, np.array([[1]])),
        (
                IMAGE_5x5_OUTER_SQUARE,
                KERNEL_3x3_SHARPEN,
                0,
                1,
                np.array([[-2, -1, -2], [-1, 0, -1], [-2, -1, -2]]),
        ),
        (
                IMAGE_5x5_OUTER_SQUARE,
                KERNEL_3x3_BLUR,
                0,
                1,
                np.array([[5 / 9, 3 / 9, 5 / 9], [3 / 9, 0, 3 / 9], [5 / 9, 3 / 9, 5 / 9]]),
        ),
        (
                IMAGE_5x5_OUTER_SQUARE,
                KERNEL_3x3_HORIZONTAL_EDGE,
                0,
                1,
                np.array([[-3, -4, -3], [0, 0, 0], [3, 4, 3]]),
        ),
        (
                IMAGE_5x5_OUTER_SQUARE,
                KERNEL_3x3_VERTICAL_EDGE,
                0,
                1,
                np.array([[-3, 0, 3], [-4, 0, 4], [-3, 0, 3]]),
        ),
        (
                IMAGE_5x5_INNER_SQUARE,
                KERNEL_3x3_SHARPEN,
                None,
                2,
                np.array([[0, -1, 0], [-1, 1, -1], [0, -1, 0]]),
        ),
        (
                IMAGE_5x5_SQUARES,
                KERNEL_3x3_HORIZONTAL_EDGE,
                None,
                2,
                np.array([[3, 2, 3], [0, 0, 0], [-3, -2, -3]]),
        ),
        (IMAGE_5x5_INNER_SQUARE, KERNEL_5x5_ONES, 0, 1, np.array([[3]])),
    ],
    ids=[
        "image and kernel of size 1x1",
        "sharpen image outer square",
        "blur image outer square",
        "find horizontal edges in image outer square",
        "find vertical edges in image outer square",
        "shapren image inner square with padding 1 and stride 2",
        "find horizontal edges in image squares with padding 1 and stride 2",
        "image and kernel of size 5x5",
    ],
)
def test_feature_map(image, kernel, padding, stride, feature_map):
    feature_map_ = convolution2D(image, kernel, padding, stride)
    np.testing.assert_array_equal(feature_map_, feature_map)


@pytest.mark.parametrize(
    "image, kernel, padding, stride, expected_exception",
    [
        ([[1, 1, 1], [2, 2, 2], [3, 3, 3]], KERNEL_3x3_BLUR, None, 1, TypeError),
        (IMAGE_256x256, [[1, 1, 1], [2, 2, 2], [3, 3, 3]], None, 1, TypeError),
        (np.ones(9), KERNEL_3x3_BLUR, None, 1, ValueError),
        (IMAGE_5x5_INNER_SQUARE, np.ones(3), None, 1, ValueError),
        (np.ones((3, 3, 3)), KERNEL_3x3_BLUR, None, 1, ValueError),
        (IMAGE_5x5_INNER_SQUARE, np.ones((3, 3, 3)), None, 1, ValueError),
        (np.array([]), KERNEL_3x3_BLUR, None, 1, ValueError),
        (IMAGE_5x5_SQUARES, np.array([]), None, 1, ValueError),
        (np.random.rand(3, 2), KERNEL_3x3_BLUR, None, 1, ValueError),
        (np.random.rand(3, 5), KERNEL_3x3_BLUR, None, 1, ValueError),
        (IMAGE_256x256, np.random.rand(33, 17), None, 1, ValueError),
        (IMAGE_256x256, np.random.rand(17, 33), None, 1, ValueError),
        (np.repeat("1", 9).reshape(3, 3), KERNEL_3x3_BLUR, None, 1, TypeError),
        (IMAGE_5x5_INNER_SQUARE, np.repeat("1", 9).reshape(3, 3), None, 1, TypeError),
        (
                np.repeat(True, 9).reshape(3, 3),
                KERNEL_3x3_HORIZONTAL_EDGE,
                None,
                1,
                TypeError,
        ),
        (IMAGE_5x5_INNER_SQUARE, np.ones((2, 2)), None, 1, ValueError),
        (IMAGE_1x1, KERNEL_5x5_ONES, None, 1, ValueError),
        (IMAGE_3x3, KERNEL_3x3_BLUR, 1.2, 1, TypeError),
        (IMAGE_3x3, KERNEL_3x3_BLUR, -1, 1, ValueError),
        (IMAGE_5x5_INNER_SQUARE, KERNEL_3x3_HORIZONTAL_EDGE, None, 0, ValueError),
        (IMAGE_5x5_INNER_SQUARE, KERNEL_3x3_SHARPEN, None, 2.2, TypeError),
    ],
    ids=[
        "image as list",
        "kernel as list",
        "1D Image",
        "1D Kernel",
        "3D Image",
        "3D Kernel",
        "0D Image",
        "0D Kernel",
        "image with smaller second dim",
        "image with smaller first dim",
        "kernel with smaller second dim",
        "kernel with smaller frst dim",
        "image with string values",
        "kernel with string values",
        "image with boolean values",
        "kernel with even size",
        "kernel size greater image size",
        "float padding",
        "negative padding",
        "zero stride",
        "float stride",
    ],
)
def test_invalid_inputs(image, kernel, padding, stride, expected_exception):
    with pytest.raises(expected_exception):
        convolution2D(image, kernel, padding, stride)
