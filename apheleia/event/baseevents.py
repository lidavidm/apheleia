from .event import Event


class ClickEvent(Event):
    def attach(self):
        self.source["window"].push_handlers(
            on_mouse_press=self.on_mouse_press,
            on_mouse_release=self.on_mouse_release)

    def detach(self):
        self.source["window"].remove_handlers(
            self.on_mouse_press,
            self.on_mouse_release)

    def on_mouse_press(self, x, y, button, mod):
        self.fire("start", x, y, button, mod)

    def on_mouse_release(self, x, y, button, mod):
        self.fire("stop", x, y, button, mod)


Event.registerImplementation("click", ClickEvent)