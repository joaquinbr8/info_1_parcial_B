import arcade
import arcade.gui  #agregar la libreria fue la unica manera que me resulto, porque tengo un problema con mi version de arcade y no puedo actualizarla, me da error y muchas incompatibilidades , no pude arreglarlo asi que vi y con esta libreria me deja correr el codigogit
import json
from tool import PencilTool, MarkerTool, SprayTool, EraserTool, BrushTool, CrayonTool

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Paint"

COLORS = {
    "black": arcade.color.BLACK,
    "red": arcade.color.RED,
    "blue": arcade.color.BLUE,
    "yellow": arcade.color.YELLOW,
    "green": arcade.color.GREEN,
}

class Paint(arcade.Window):
    def __init__(self, load_path: str = None):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.current_background_color = arcade.color.WHITE  
        arcade.set_background_color(self.current_background_color)  

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        self.create_tool_buttons()

        
        self.create_color_buttons()

    
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left", 
                anchor_y="top", 
                child=self.v_box
            )
        )

        self.tool = PencilTool()
        self.used_tools = {self.tool.name: self.tool}
        self.color = arcade.color.BLUE
        if load_path is not None:
            with open(load_path, 'r') as file:
                self.traces = json.load(file)
        else:
            self.traces = []

    def create_tool_buttons(self):
        pencil_button = arcade.gui.UIFlatButton(text="Pencil", width=100)
        pencil_button.on_click = self.set_tool_pencil
        self.v_box.add(pencil_button.with_space_around(bottom=10))

        marker_button = arcade.gui.UIFlatButton(text="Marker", width=100)
        marker_button.on_click = self.set_tool_marker
        self.v_box.add(marker_button.with_space_around(bottom=10))

        spray_button = arcade.gui.UIFlatButton(text="Spray", width=100)
        spray_button.on_click = self.set_tool_spray
        self.v_box.add(spray_button.with_space_around(bottom=10))

        eraser_button = arcade.gui.UIFlatButton(text="Eraser", width=100)
        eraser_button.on_click = self.set_tool_eraser
        self.v_box.add(eraser_button.with_space_around(bottom=10))

        brush_button = arcade.gui.UIFlatButton(text="Brush", width=100)
        brush_button.on_click = self.set_tool_brush
        self.v_box.add(brush_button.with_space_around(bottom=10))

        crayon_button = arcade.gui.UIFlatButton(text="Crayon", width=100)
        crayon_button.on_click = self.set_tool_crayon
        self.v_box.add(crayon_button.with_space_around(bottom=10))

    def create_color_buttons(self):
        for color_name, color_value in COLORS.items():
            color_button = arcade.gui.UIFlatButton(text=color_name.capitalize(), width=100)
            color_button.on_click = lambda event, color=color_value: self.set_color(color)
            self.v_box.add(color_button.with_space_around(bottom=10))


    def set_tool_pencil(self, event):
        self.tool = PencilTool()
        self.used_tools[self.tool.name] = self.tool

    def set_tool_marker(self, event):
        self.tool = MarkerTool(width=10)
        self.used_tools[self.tool.name] = self.tool

    def set_tool_spray(self, event):
        self.tool = SprayTool(radius=15, points=30)
        self.used_tools[self.tool.name] = self.tool

    def set_tool_eraser(self, event):
        self.tool = EraserTool(size=15)
        self.used_tools[self.tool.name] = self.tool

    def set_tool_brush(self, event):
        self.tool = BrushTool(width=8)
        self.used_tools[self.tool.name] = self.tool

    def set_tool_crayon(self, event):
        self.tool = CrayonTool(width=4)
        self.used_tools[self.tool.name] = self.tool

    def set_color(self, color):
        self.color = color

    def fill_background(self):
        self.current_background_color = self.color
        arcade.set_background_color(self.current_background_color)
        self.traces = []  

    def clear_background(self):
        
        self.current_background_color = arcade.color.WHITE
        arcade.set_background_color(self.current_background_color)
        self.traces = []  

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1:
            self.tool = PencilTool()
        elif symbol == arcade.key.KEY_2:
            self.tool = MarkerTool(width=10)
        elif symbol == arcade.key.KEY_3:
            self.tool = SprayTool(radius=15, points=30)
        elif symbol == arcade.key.KEY_4:
            self.tool = EraserTool(size=15)
        elif symbol == arcade.key.KEY_5:
            self.tool = BrushTool(width=8)
        elif symbol == arcade.key.KEY_6:
            self.tool = CrayonTool(width=4)

        elif symbol == arcade.key.A:
            self.color = arcade.color.RED
        elif symbol == arcade.key.S:
            self.color = arcade.color.GREEN
        elif symbol == arcade.key.D:
            self.color = arcade.color.BLUE
        elif symbol == arcade.key.T:  
            self.color = arcade.color.YELLOW

        elif symbol == arcade.key.F:  
            self.fill_background()

        elif symbol == arcade.key.U:  
            self.clear_background()

        elif symbol == arcade.key.O:
            with open('drawing.txt', 'w') as file:
                json.dump(self.traces, file)

        self.used_tools[self.tool.name] = self.tool
        print(self.used_tools, self.tool)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(x, y)
        if button == arcade.MOUSE_BUTTON_LEFT:
            if isinstance(self.tool, EraserTool):
                self.tool.erase_trace(x, y, self.traces)
            else:
                self.traces.append({"tool": self.tool.name, "color": self.color, "trace": [(x, y)]})

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if self.traces:
            self.traces[-1]["trace"].append((x, y))

    def on_draw(self):
        arcade.start_render()
        
        arcade.set_background_color(self.current_background_color)
        self.manager.draw()  
        for tool in self.used_tools.values():
            tool.draw_traces(self.traces)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        app = Paint(sys.argv[1])
    else:
        app = Paint()
    arcade.run()
