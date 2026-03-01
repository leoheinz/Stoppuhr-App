from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class Stopwatch(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.time = 0
        self.running = False

        # Anzeige der Zeit
        self.time_label = Label(
            text="00:00.0",
            font_size=50,
            size_hint=(1, 0.3)
        )
        self.add_widget(self.time_label)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2))

        start_btn = Button(text="Start")
        start_btn.bind(on_press=self.start)

        stop_btn = Button(text="Stop")
        stop_btn.bind(on_press=self.stop)

        lap_btn = Button(text="Lap")
        lap_btn.bind(on_press=self.lap)

        reset_btn = Button(text="Reset")
        reset_btn.bind(on_press=self.reset)

        button_layout.add_widget(start_btn)
        button_layout.add_widget(stop_btn)
        button_layout.add_widget(lap_btn)
        button_layout.add_widget(reset_btn)

        self.add_widget(button_layout)

        # Liste für Zwischenzeiten
        self.scroll = ScrollView(size_hint=(1, 0.5))
        self.lap_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None
        )
        self.lap_list.bind(
            minimum_height=self.lap_list.setter("height")
        )

        self.scroll.add_widget(self.lap_list)
        self.add_widget(self.scroll)

    # Zeitformat
    def format_time(self, t):
        minutes = int(t // 60)
        seconds = int(t % 60)
        tenths = int((t * 10) % 10)
        return f"{minutes:02}:{seconds:02}.{tenths}"

    # Update jede 0.1 Sekunde
    def update(self, dt):
        if self.running:
            self.time += dt
            self.time_label.text = self.format_time(self.time)

    def start(self, instance):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update, 0.1)

    def stop(self, instance):
        self.running = False

    def reset(self, instance):
        self.running = False
        self.time = 0
        self.time_label.text = "00:00.0"
        self.lap_list.clear_widgets()

    def lap(self, instance):
        lap_time = self.format_time(self.time)
        label = Label(
            text=f"Zwischenzeit: {lap_time}",
            size_hint_y=None,
            height=40
        )
        self.lap_list.add_widget(label)


class StopwatchApp(App):
    def build(self):
        return Stopwatch()


if __name__ == "__main__":
    StopwatchApp().run()