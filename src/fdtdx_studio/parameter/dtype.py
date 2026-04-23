from enum import Enum

class DType(Enum):
    """Enum for different options for the Datattype of the Simulation e.g Float32"""
    Float_32 = "jax.numpy.float32"
    Float_64 = "jax.numpy.float64"