from wgpu import BufferUsage, GPUTexture, IndexFormat, VertexFormat
from gpu import (
    GraphicPipelineBuilder,
    BufferBuilder,
    CommandBufferBuilder,
    TextureBuilder,
)
from window import Window
import numpy as np


class MyApp(Window):
    def setup(self, size: tuple[int, int]):
        self.with_title("Hello Cube")

        # fmt: off
        vertex_data = np.array(
            [
                # x, y, z, r, g, b
                [0.5, 0.5, 0.5, 1.0, 0.0, 0.0],
                [-0.5, 0.5, 0.5, 1.0, 0.0, 0.0],
                [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0],
                [0.5, -0.5, 0.5, 1.0, 0.0, 0.0],

                [0.5, 0.5, 0.5, 0.0, 1.0, 0.0],
                [0.5, -0.5, 0.5, 0.0, 1.0, 0.0],
                [0.5, -0.5, -0.5, 0.0, 1.0, 0.0],
                [0.5, 0.5, -0.5, 0.0, 1.0, 0.0],

                [0.5, 0.5, -0.5, 0.0, 0.0, 1.0],
                [0.5, -0.5, -0.5, 0.0, 0.0, 1.0],
                [-0.5, -0.5, -0.5, 0.0, 0.0, 1.0],
                [-0.5, 0.5, -0.5, 0.0, 0.0, 1.0],

                [-0.5, 0.5, 0.5, 1.0, 1.0, 0.0],
                [-0.5, 0.5, -0.5, 1.0, 1.0, 0.0],
                [-0.5, -0.5, -0.5, 1.0, 1.0, 0.0],
                [-0.5, -0.5, 0.5, 1.0, 1.0, 0.0],

                [0.5, 0.5, 0.5, 0.0, 1.0, 1.0],
                [0.5, 0.5, -0.5, 0.0, 1.0, 1.0],
                [-0.5, 0.5, -0.5, 0.0, 1.0, 1.0],
                [-0.5, 0.5, 0.5, 0.0, 1.0, 1.0],
    
                [0.5, -0.5, 0.5, 1.0, 0.0, 1.0],
                [-0.5, -0.5, 0.5, 1.0, 0.0, 1.0],
                [-0.5, -0.5, -0.5, 1.0, 0.0, 1.0],
                [0.5, -0.5, -0.5, 1.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )

        index_data = np.array(
            [
                 0,  1,  2,  0,  2,  3,
                 4,  5,  6,  4,  6,  7,
                 8,  9, 10,  8, 10, 11,
                12, 13, 14, 12, 14, 15,
                16, 17, 18, 16, 18, 19,
                20, 21, 22, 20, 22, 23,
            ],
            dtype=np.uint32,
        )
        # fmt: on

        self.vertex_buffer = (
            BufferBuilder()
            .from_data(vertex_data)
            .with_usage(BufferUsage.VERTEX)
            .build()
        )

        self.index_buffer = (
            BufferBuilder().from_data(index_data).with_usage(BufferUsage.INDEX).build()
        )

        self.depth_texture = TextureBuilder().build_depth(size)

        self.pipeline = (
            GraphicPipelineBuilder()
            .with_shader("cube.wgsl")
            .with_depth_stencil()
            .with_vertex_buffer()
            .with_attribute(VertexFormat.float32x3)
            .with_attribute(VertexFormat.float32x3)
            .build()
        )

    def render(self, screen: GPUTexture):
        command_buffer_builder = CommandBufferBuilder()

        render_pass = (
            command_buffer_builder.begin_render_pass(screen)
            .with_depth_stencil(self.depth_texture)
            .build()
        )
        render_pass.set_pipeline(self.pipeline)
        render_pass.set_vertex_buffer(0, self.vertex_buffer)
        render_pass.set_index_buffer(self.index_buffer, IndexFormat.uint32)  # type: ignore
        render_pass.draw_indexed(36)
        render_pass.end()

        command_buffer_builder.submit()


MyApp().run()