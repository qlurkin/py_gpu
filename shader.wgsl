struct VertexInput {
    @builtin(vertex_index) vertex_index : u32,
};
struct VertexOutput {
    @location(0) color : vec4<f32>,
    @builtin(position) pos: vec4<f32>,
};

@vertex
fn vs_main(in: VertexInput) -> VertexOutput {
    var positions = array<vec2<f32>, 3>(
        vec2<f32>(0.0, -0.5),
        vec2<f32>(0.5, 0.5),
        vec2<f32>(-0.5, 0.75),
    );
    var colors = array<vec3<f32>, 3>(  // srgb colors
        vec3<f32>(1.0, 1.0, 0.0),
        vec3<f32>(1.0, 0.0, 1.0),
        vec3<f32>(0.0, 1.0, 1.0),
    );
    let index = i32(in.vertex_index);
    var out: VertexOutput;
    out.pos = vec4<f32>(positions[index], 0.0, 1.0);
    out.color = vec4<f32>(colors[index], 1.0);
    return out;
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let physical_color = pow(in.color.rgb, vec3<f32>(2.2));  // gamma correct
    return vec4<f32>(physical_color, in.color.a);
}
