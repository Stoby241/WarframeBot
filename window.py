from kivy.app import App
from kivy.uix.widget import Widget


class WarframeBot(Widget):
    pass


class WarframeBotApp(App):
    def build(self):
        return WarframeBot()


if __name__ == '__main__':
    WarframeBotApp().run()
