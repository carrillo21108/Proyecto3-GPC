#En OpenGL, los shaders se escriben enn un
#nuevo lenguaje de programacion llamada GLSL
#Graphics Library Shader Language

vertex_shader = '''
#version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 outNormals;
out vec3 outPosition;

void main()
{
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(position,1.0);
    UVs = texCoords;
    outNormals = (modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    outPosition = position;
}
'''

fat_vertex_shader = '''
#version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float fatnessFrecuency;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    float fatness = sin(fatnessFrecuency*time);
    if (fatness < 0.0)
        fatness = 0.0;
    outNormals  =(modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = position+(fatness/4)*outNormals;
    
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(pos,1.0);
    UVs = texCoords;
}
'''

toon_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    if (intensity<0.33)
        intensity=0.2;
    else if (intensity<0.66)
        intensity=0.6;
    else
        intensity=1.0;
    fragColor = texture(tex,UVs)*intensity;
}

'''

gourad_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    fragColor = texture(tex,UVs)*intensity;
}

'''

unlit_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex,UVs);
}

'''

colors_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform float time;

in vec3 outNormals;

out vec4 fragColor;

void main()
{
    
    vec3 dir1 = vec3(sin(time),0,cos(time)); 
    vec3 dir2 = vec3(cos(time),0,sin(time));
    vec3 dir3 = vec3(0,sin(time),cos(time));
    
    float diffuse1 = pow(dot(outNormals,dir1),2.0);
    float diffuse2 = pow(dot(outNormals,dir2),2.0);
    float diffuse3 = pow(dot(outNormals,dir3),2.0);
    
    vec3 col1 = diffuse1 * vec3(1,0,0);
    vec3 col2 = diffuse2 * vec3(0,0,1);
    vec3 col3 = diffuse3 * vec3(0,1,0);
    
    fragColor = vec4(col1 + col2 + col3, 1.0);
}

'''

stripes_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform float time;

in vec2 UVs;
in vec3 outNormals;
in vec3 outPosition;

out vec4 fragColor;

void main()
{
    if (cos(100*outPosition.y+10*time)<0.0)
        discard;
    
    fragColor = texture(tex,UVs);
}

'''

pencil_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec3 outNormals;
in vec3 outPosition;

out vec4 fragColor;

float horizontalLine(vec2 pixel, float y_pos, float width) {
    return 1.0 - smoothstep(-1.0, 1.0, abs(pixel.y - y_pos) - 0.5 * width);
}

void main()
{
    float df = dot(normalize(outNormals), normalize(-dirLight));
    vec2 pos = gl_FragCoord.xy;
    
    float line_width = 7.0 * (1.0 - smoothstep(0.0, 0.3, df)) + 0.5;
    float lines_sep = 6.0;
    vec2 grid_pos = vec2(pos.x, mod(pos.y, lines_sep));
    float line_1 = horizontalLine(grid_pos, lines_sep / 2.0, line_width);
    grid_pos.y = mod(pos.y + lines_sep / 2.0, lines_sep);
    float line_2 = horizontalLine(grid_pos, lines_sep / 2.0, line_width);
    
    lines_sep = 4.0;
    grid_pos = vec2(pos.x, mod(pos.y, lines_sep));
    float line_3 = horizontalLine(grid_pos, lines_sep / 2.0, line_width);
    grid_pos.y = mod(pos.y + lines_sep / 2.0, lines_sep);
    float line_4 = horizontalLine(grid_pos, lines_sep / 2.0, line_width);
    
    float surface_color = 1.0;
    surface_color -= line_1 * (1.0 - smoothstep(0.5, 0.75, df));
    surface_color -= line_2 * (1.0 - smoothstep(0.4, 0.5, df));
    surface_color -= line_3 * (1.0 - smoothstep(0.4, 0.65, df));
    surface_color -= line_4 * (1.0 - smoothstep(0.2, 0.4, df));
    surface_color = clamp(surface_color, 0.05, 1.0);
    
    fragColor = vec4(vec3(surface_color), 1.0);
}

'''

dot_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec3 outNormals;
in vec3 outPosition;

out vec4 fragColor;

float circle(vec2 pixel, vec2 center, float radius) {
    return 1.0 - smoothstep(radius - 1.0, radius + 1.0, length(pixel - center));
}

void main()
{
    float df = dot(normalize(outNormals), normalize(-dirLight));
    vec2 pos = gl_FragCoord.xy;
    
    float grid_step = 12.0;
    vec2 grid_pos = mod(pos, grid_step);

    float surface_color = 1.0;
    surface_color -= circle(grid_pos, vec2(grid_step / 2.0), 0.8 * grid_step * pow(1.0 - df, 2.0));
    surface_color = clamp(surface_color, 0.05, 1.0);
    
    fragColor = vec4(vec3(surface_color), 1.0);
}

'''

yellow_glow_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    fragColor = texture(tex,UVs)*intensity;
}

'''

skybox_vertex_shader = '''
#version 450 core
layout (location=0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    gl_Position = projectionMatrix*viewMatrix*vec4(inPosition,1.0);
}
'''

skybox_fragment_shader = '''
#version 450 core

uniform samplerCube skybox;

in vec3 texCoords;

out vec4 fragColor;

void main()
{
    fragColor = texture(skybox,texCoords);
}

'''