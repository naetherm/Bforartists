
#define VERTEX_ACTIVE   1 << 0
#define VERTEX_SELECTED 1 << 1
#define ACTIVE_NURB     1 << 2 /* Keep the same value of `ACTIVE_NURB` in `draw_cache_imp_curve.c` */
#define EVEN_U_BIT      1 << 3

layout(lines) in;
layout(triangle_strip, max_vertices = 10) out;

uniform vec2 viewportSize;
uniform bool showCurveHandles;

flat in int vertFlag[];

out vec4 finalColor;

void output_line(vec2 offset, vec4 color)
{
	finalColor = color;

	gl_Position = gl_in[0].gl_Position;
	gl_Position.xy += offset * gl_in[0].gl_Position.w;
	EmitVertex();

	gl_Position = gl_in[1].gl_Position;
	gl_Position.xy += offset * gl_in[1].gl_Position.w;
	EmitVertex();
}

void main()
{
	vec4 v1 = gl_in[0].gl_Position;
	vec4 v2 = gl_in[1].gl_Position;

	int is_active_nurb = (vertFlag[1] & ACTIVE_NURB);
	int color_id = (vertFlag[1] >> 4);

	/* Don't output any edges if we don't show handles */
	if (!showCurveHandles && (color_id < 5))
		return;

	bool edge_selected = (((vertFlag[1] | vertFlag[0]) & VERTEX_SELECTED) != 0);

	vec4 inner_color;
	if      (color_id == 0) inner_color = (edge_selected) ? colorHandleSelFree : colorHandleFree;
	else if (color_id == 1) inner_color = (edge_selected) ? colorHandleSelAuto : colorHandleAuto;
	else if (color_id == 2) inner_color = (edge_selected) ? colorHandleSelVect : colorHandleVect;
	else if (color_id == 3) inner_color = (edge_selected) ? colorHandleSelAlign : colorHandleAlign;
	else if (color_id == 4) inner_color = (edge_selected) ? colorHandleSelAutoclamp : colorHandleAutoclamp;
	else {
		bool is_selected = (((vertFlag[1] & vertFlag[0]) & VERTEX_SELECTED) != 0);
		bool is_u_segment = (((vertFlag[1] ^ vertFlag[0]) & EVEN_U_BIT) != 0);
		if (is_u_segment) {
			inner_color = (is_selected) ? colorNurbSelUline : colorNurbUline;
		}
		else {
			inner_color = (is_selected) ? colorNurbSelVline : colorNurbVline;
		}
	}

	vec4 outer_color = (is_active_nurb != 0)
	                   ? mix(colorActiveSpline, inner_color, 0.25) /* Minimize active color bleeding on inner_color. */
	                   : vec4(inner_color.rgb, 0.0);

	vec2 v1_2 = (v2.xy/v2.w - v1.xy/v1.w);
	vec2 offset = sizeEdge * 4.0 / viewportSize; /* 4.0 is eyeballed */

	if (abs(v1_2.x * viewportSize.x) < abs(v1_2.y * viewportSize.y)) {
		offset.y = 0.0;
	}
	else {
		offset.x = 0.0;
	}

	/* draw the transparent border (AA). */
	if (is_active_nurb != 0) {
		offset *= 0.75; /* Don't make the active "halo" appear very thick. */
		output_line(offset * 2.0, vec4(colorActiveSpline.rgb, 0.0));
	}

	/* draw the outline. */
	output_line(offset, outer_color);

	/* draw the core of the line. */
	output_line(vec2(0.0), inner_color);

	/* draw the outline. */
	output_line(-offset, outer_color);

	/* draw the transparent border (AA). */
	if (is_active_nurb != 0) {
		output_line(offset * -2.0, vec4(colorActiveSpline.rgb, 0.0));
	}

	EndPrimitive();
}
