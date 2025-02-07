import numpy as np
import wgpu
from wgut.auto_compute_pipeline import AutoComputePipeline
from wgut.builders import read_buffer


computer = AutoComputePipeline("./compute.slang")

rng = np.random.default_rng()

numpy_data = rng.random(size=12800, dtype=np.float32)
print(numpy_data)
computer.set_array(0, 0, numpy_data)

numpy_data = rng.random(size=12800, dtype=np.float32)
print(numpy_data)
computer.set_array(0, 1, numpy_data)


buffer_res = computer.set_array(
    0, 2, np.zeros(12800, dtype=np.float32), wgpu.BufferUsage.COPY_SRC
)


computer.dispatch(12800 // 64)

out = read_buffer(buffer_res)

result = np.frombuffer(out.cast("f"), dtype=np.float32)

print(result)
