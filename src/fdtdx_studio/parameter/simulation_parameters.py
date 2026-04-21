from typing import Literal, cast

import jax
import fdtdx
import jax.numpy as jnp
from fdtdx_studio.parameter.DType import DType

DTYPE_MAP = {
    "jax.numpy.float32": jnp.float32,
    "jax.numpy.float64": jnp.float64
}
class simulation_parameters:
  """Class for the needed simulation Parameters"""

  def __init__(self):
    """Initializes a Project with standard Values for Parameters"""
    self.time = 100e-15
    self.resolution = 100e-9
    self.backend: str = 'gpu'
    self.dtype = DType.Float_32
    self.courant_factor = 0.99
    self.gradient_config = None # not needed in our implementation
    self.key = jax.random.PRNGKey(seed=42)

        
  def set_time(self, time):
    """set time to the given value"""
    self.time= time

  def set_resolution(self, resolution):
    """set resolution to the given value"""
    self.resolution= resolution

  def set_backend(self, backend: str):
    """set backend to the given value"""
    self.backend = backend

  def set_dtype(self, Dtype: DType):
    """set DType to the given value"""
    self.dtype = Dtype

  def set_courant_factor(self, courant_factor):
    """set courant factor to the given value"""
    self.courant_factor = courant_factor

  VALID_BACKENDS: dict[Literal["gpu", "tpu", "cpu", "METAL"], Literal["gpu", "tpu", "cpu", "METAL"]] = {"gpu": "gpu", "tpu": "tpu", "cpu": "cpu", "METAL": "METAL"}
  def config(self):
    """FDTDX method for Parameters"""
    if self.backend not in self.VALID_BACKENDS:
      raise ValueError(f"Invalid backend: {self.backend}")
    backend_key = cast(Literal["gpu", "tpu", "cpu", "METAL"], self.backend)
    return fdtdx.SimulationConfig(
      time= self.time,
      resolution= self.resolution,
      backend= self.VALID_BACKENDS[backend_key],  
      dtype= DTYPE_MAP[self.dtype.value],
      courant_factor= self.courant_factor,
      gradient_config= self.gradient_config,
    )
