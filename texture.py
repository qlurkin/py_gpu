from wgpu import BufferUsage, GPUTexture, VertexFormat
from gpu import (
    BindGroupBuilder,
    GraphicPipelineBuilder,
    BufferBuilder,
    CommandBufferBuilder,
    TextureBuilder,
)
from window import Window
import numpy as np


class MyApp(Window):
    def setup(self):
        self.set_title("Hello Texture")
        vertex_data = np.array(
            [
                # x, y, u, v
                [0.0, 0.5, 0.5, 0.0],
                [-0.5, -0.5, 0.0, 1.0],
                [0.5, -0.5, 1.0, 1.0],
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
            GraphicPipelineBuilder(self.get_texture_format())
            .with_shader("texture.wgsl")
            .with_vertex_buffer()
            .with_attribute(VertexFormat.float32x2)
            .with_attribute(VertexFormat.float32x2)
            .build()
        )

        diffuse_texture = TextureBuilder().from_file("wood.jpg")

        self.bind_group = (
            BindGroupBuilder(self.pipeline.get_bind_group_layout(0))
            .with_texture_binding(diffuse_texture)
            .with_sampler_binding()
            .build()
        )

    def render(self, screen: GPUTexture):
        command_buffer_builder = CommandBufferBuilder()

        render_pass = command_buffer_builder.begin_render_pass(screen).build()
        render_pass.set_pipeline(self.pipeline)
        render_pass.set_vertex_buffer(0, self.vertex_buffer)
        render_pass.set_bind_group(0, self.bind_group)
        render_pass.draw(3)
        render_pass.end()

        command_buffer_builder.submit()


MyApp().run()