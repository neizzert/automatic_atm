from flet import (
    Container,
    Colors,
    border,
    Row,
    VerticalDivider,
    MainAxisAlignment,

)

class MoneyBillet(Container):
    def __init__(self, x, y):
        super().__init__()
        self.width = 100
        self.height = 50
        self.padding=4
        self.bgcolor = Colors.LIGHT_GREEN_ACCENT_700
        self.left = x
        self.top = y
        self.border_radius = 5
        self.border = border.all(2, Colors.BLACK87)

        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                VerticalDivider(
                    color=Colors.BLACK87,
                    width=2
                ),
                Container(
                    width=40,
                    height=20,
                    border=border.all(2, Colors.BLACK87)
                ),
                VerticalDivider(
                    color=Colors.BLACK87,
                    width=2
                )
            ]
        )