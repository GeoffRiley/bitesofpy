import math
from typing import Tuple, Union, List


class Vector:
    """A class for representing 3D vectors represented by three coordinates."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, coords: List[float]) -> "Vector":
        """Create a new Vector from a list of numbers.

        Args:
            coords: The coordinates of the new vector as list.

        Returns:
            A new vector with the coordinates as x,y,z.
        """
        return cls(*coords)

    def norm(self, p: int) -> float:
        """Return the p-norm of the Vector.

        For p=2 it returns the standard l2-norm, i.e. the length of the Vector.

        Args:
            p: The p-value to calculate the norm. Should be a real positive integer.

        Returns:
            The value of the p-norm for this Vector.
        """
        return sum(c ** p for c in self()) ** (1 / p)

    def iscollinear(self, other: "Vector") -> bool:
        """Test another Vector for collinearity.

        Args:
            other: The other Vector.

        Returns:
            True, if self is collinear to other, False otherwise.
        """
        return len(set(v / w for v, w in zip(self(), other()))) == 1

    def angle(self, other: "Vector") -> float:
        """Return the angle between two vectors.

        Args:
            other: The other Vector.

        Returns:
            The angle between self and other.
        """
        return math.acos((self * other) / (self.norm(2) * other.norm(2)))

    def __getitem__(self, index: int) -> float:
        return self()[index]

    def __call__(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    def __len__(self) -> int:
        return len(self())

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union[float, "Vector"]) -> Union[float, "Vector"]:
        if isinstance(other, Vector):
            return sum(v * w for v, w in zip(self(), other()))

        try:
            other = float(
                other
            )  # cannot easily check for int, float as isinstance(int, float) is False
            return Vector(self.x * other, self.y * other, self.z * other)
        except ValueError:
            print("Cannot deal with values other than Vectors and numbers.")
            return self

    def __rmul__(self, other: Union[float, "Vector"]) -> Union[float, "Vector"]:
        return self.__mul__(other)

    def __str__(self) -> str:
        return f"[{self.x} {self.y} {self.z}]"

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"


if __name__ == "__main__":
    v = Vector(1, 1, 1)
    print(v)
    print(v.__repr__())
    print(len(v))
    print(v.x, v.y, v.z)
    print(v[0], v[1], v[2])
    print(v())
    print(v.norm(1), v.norm(2), v.norm(3))

    w = Vector.from_list([1, 2, 3])
    print(w)

    print(v + w)
    print(w + v)
    print(w - v)

    print(v * 2)
    print(2 * v)
    print(v * 0.5)
    print(v * w)
    print(w * v)

    print(v.iscollinear(w))
    print(v.iscollinear(Vector(2, 2, 2)))

    print(Vector(10, 9, 3).angle(Vector(2, 5, 12)))

    v = Vector(0, 3, 2)
    w = Vector(4, 1, 1)
    u = Vector(0, -2, 0)
    x = 3 * v - 2 * w + 4 * u
    print(x)
