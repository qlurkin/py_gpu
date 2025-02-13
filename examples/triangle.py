from wgpu import BufferUsage, GPUTexture, VertexFormat
from wgut.builders import (
    RenderPipelineBuilder,
    BufferBuilder,
    CommandBufferBuilder,
    print_adapter_info,
)
from wgut.window import Window
import numpy as np


class MyApp(Window):
    def setup(self):
        print_adapter_info()
        self.set_title("Hello Triangle")
        vertex_data = np.array(
            [
                # x, y, r, g, b
                [0.0, 0.5, 1.0, 0.0, 0.0],
                [-0.5, -0.5, 0.0, 1.0, 0.0],
                [0.5, -0.5, 0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )

        self.vertex_buffer = (
            BufferBuilder()
            .from_data(vertex_data)
            .with_usage(BufferUsage.VERTEX)
            .build()
        )

        self.pipeline = (
            RenderPipelineBuilder(self.get_texture_format())
            .with_shader("triangle.wgsl")
            .with_vertex_buffer()
            .with_attribute(VertexFormat.float32x2)
            .with_attribute(VertexFormat.float32x3)
            .build()
        )

    def render(self, screen: GPUTexture):
        command_buffer_builder = CommandBufferBuilder()

        render_pass = command_buffer_builder.begin_render_pass(screen).build()
        render_pass.set_pipeline(self.pipeline)
        render_pass.set_vertex_buffer(0, self.vertex_buffer)
        render_pass.draw(3)
        render_pass.end()

        command_buffer_builder.submit()


MyApp().run()
