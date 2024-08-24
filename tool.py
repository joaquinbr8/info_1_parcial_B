import arcade
import random

class PencilTool:
    name = "Pencil"

    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] == self.name:
                arcade.draw_lines(trace["trace"], trace["color"], 2)

class MarkerTool:
    name = "Marker"

    def __init__(self, width=10):
        self.width = width

    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] == self.name:
                arcade.draw_line_strip(trace["trace"], trace["color"], self.width)

class SprayTool:
    name = "Spray"

    def __init__(self, radius=15, points=30):
        self.radius = radius
        self.points = points

    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] == self.name:
                for x, y in trace["trace"]:
                    for _ in range(self.points):
                        offset_x = random.randint(-self.radius, self.radius)
                        offset_y = random.randint(-self.radius, self.radius)
                        if offset_x**2 + offset_y**2 <= self.radius**2:
                            arcade.draw_point(x + offset_x, y + offset_y, trace["color"], 1)

class EraserTool:
    name = "Eraser"

    def __init__(self, size=15):
        self.size = size

    def erase_trace(self, x, y, traces):
        erased_traces = []
        for trace in traces:
            trace_copy = trace.copy()
            trace_copy["trace"] = [point for point in trace["trace"] if not (x - self.size < point[0] < x + self.size and y - self.size < point[1] < y + self.size)]
            if trace_copy["trace"]:
                erased_traces.append(trace_copy)
        traces.clear()
        traces.extend(erased_traces)

    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] == self.name:
                arcade.draw_line_strip(trace["trace"], arcade.color.WHITE, self.size)

class BrushTool:
    name = "Brush"

    def __init__(self, width=8):
        self.width = width

    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] == self.name:
                for x, y in trace["trace"]:
                    offset_x = random.randint(-self.width, self.width)
                    offset_y = random.randint(-self.width, self.width)
                    arcade.draw_circle_filled(x + offset_x, y + offset_y, self.width / 2, trace["color"])

class CrayonTool:
    name = "Crayon"

    def __init__(self, width=4):
        self.width = width

    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] == self.name:
                for x, y in trace["trace"]:
                    offset_x = random.randint(-self.width, self.width)
                    offset_y = random.randint(-self.width, self.width)
                    arcade.draw_line(x, y, x + offset_x, y + offset_y, trace["color"], self.width)
