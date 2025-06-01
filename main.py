from flet import *
from time import sleep
from billet import MoneyBillet

def main(page:Page):
        page.vertical_alignment = MainAxisAlignment.CENTER
        page.horinzontal_alignment = CrossAxisAlignment.CENTER
        page.bgcolor = 'black'
        
        def write_numbers_at_screen(e):
            nonlocal text

            if not current_mode.value:
                display_screen.content = text_error
                page.update()
                sleep(1)
                display_screen.content = column_content
                page.update()
            else:
                text.value += e.control.text
                if text.value[0] == '0' or text.value[0:2] == "00" or text.value[0:3] == '000':
                    display_screen.content = text_error
                    page.update()
                    sleep(1)
                    text.value = ''
                    display_screen.content = column_content
                    page.update()
                    return
                page.update()

        def clear_screen(e):
            if display_screen.content == column_content:
                text.value = ''
                page.update()
            else:
                return

        def block_buttons(enable):
            if enable:
                for number_button in container_numbers.content.controls: number_button.disabled = True
                for mode_button in container_modes.content.controls: mode_button.disabled = True
                for operation_button in container_operations.content.controls:
                    if operation_button.text in ['CLEAR', 'CANCEL', 'CONFIRM']:
                        operation_button.disabled = True
            else:
                for number_button in container_numbers.content.controls: number_button.disabled = False
                for mode_button in container_modes.content.controls: mode_button.disabled = False
                for operation_button in container_operations.content.controls:
                    if operation_button.text in ['CLEAR', 'CANCEL', 'CONFIRM']:
                        operation_button.disabled = False

        def initialize_the_machine():
            display_screen.content = column_content
            display_screen.bgcolor = Colors.LIGHT_GREEN_ACCENT_200

        def turn_off(e):
            if display_screen.data == 1:
                display_screen.bgcolor = Colors.LIGHT_GREEN_100
                display_screen.content = None
                display_screen.data = 0
                block_buttons(True)
                reset_content_screen()
                page.update()
            else:
                display_screen.data = 1
                initialize_the_machine()
                block_buttons(False)
                page.update()

        def extract_money():
            # Previously, we know where the elements (x, y) should be in the base. 
            # Therefore, we define a set of elements with a fixed position Y.
            for billet in [
                MoneyBillet(x=(300 - 100) / 2, y=125),
                MoneyBillet(x=(300 - 100) / 2, y=115),
                MoneyBillet(x=(300 - 100) / 2, y=105),
                MoneyBillet(x=(300 - 100) / 2, y=95),
                MoneyBillet(x=(300 - 100) / 2, y=86)
            ]:
                container_extraction_and_outlet_accessory.content.controls.append(billet)

            page.update()

            sleep(1)
            # We put the operations and numbers in pause block_buttons
            for button_number in container_numbers.content.controls:
                button_number.disabled = True

            for button_operation in container_operations.content.controls:
                if button_operation.text in ['OFF', 'CANCEL', 'CONFIRM']:
                    button_operation.disabled = True
            page.update()

            length = len(container_extraction_and_outlet_accessory.content.controls) - 1

            while length > 1:
                delta_y = container_extraction_and_outlet_accessory.content.controls[length].top
                while delta_y > 5:
                    delta_y -= 10
                    container_extraction_and_outlet_accessory.content.controls[length].top = delta_y
                    page.update()
                    sleep(0.10)
                container_extraction_and_outlet_accessory.content.controls[length].visible = False
                page.update()

                container_extraction_and_outlet_accessory.content.controls.pop(length)
                length -= 1

            for button_number in container_numbers.content.controls:
                button_number.disabled = False

            for button_operation in container_operations.content.controls:
                if button_operation.text in ['OFF', 'CANCEL', 'CONFIRM']:
                    button_operation.disabled = False
            page.update()


        def reset_content_screen():
            current_mode.value = ''
            text.value = ''
            display_screen.content = column_content

        def cancel_operation(e):
            reset_content_screen()

            for button in container_modes.content.controls:
                if button.disabled:
                    button.disabled = False
                else:
                    continue
            page.update()

        def show_billets():
            auto_y = 125

            for button_number in container_numbers.content.controls:
                button_number.disabled = True

            for button_operation in container_operations.content.controls:
                if button_operation.text in ['OFF', 'CANCEL', 'CONFIRM']:
                    button_operation.disabled = True

            for billet in [
                    MoneyBillet(x=(300 - 100) / 2, y=5), 
                    MoneyBillet(x=(300 - 100) / 2, y=5), 
                    MoneyBillet(x=(300 - 100) / 2, y=5), 
                    MoneyBillet(x=(300 - 100) / 2, y=5), 
                    MoneyBillet(x=(300 - 100) / 2, y=5) 
                ]:

                delta_y = 5
                container_extraction_and_outlet_accessory.content.controls.append(billet)
                while delta_y < auto_y:
                        delta_y += 10
                        billet.top = delta_y
                        page.update()
                        sleep(0.09)                    
                delta_y = 5
                auto_y -= 10

            sleep(1)

            for button_number in container_numbers.content.controls:
                button_number.disabled = False

            for button_operation in container_operations.content.controls:
                if button_operation.text in ['OFF', 'CANCEL', 'CONFIRM']:
                    button_operation.disabled = False

            length = len(container_extraction_and_outlet_accessory.content.controls) - 1

            while length > 1:
                container_extraction_and_outlet_accessory.content.controls[length].visible = False
                page.update()
                sleep(0.10)

                # we free up unnecessary space
                container_extraction_and_outlet_accessory.content.controls.pop(length)
                length -= 1

        def execute_operation(e):
            nonlocal bank_account

            if current_mode.value == '':
                display_screen.content = text_error
                page.update()
                sleep(1)
                display_screen.content = None
                page.update()
            else:
                if current_mode.value == MODES['1']:
                    if text.value == '':
                        display_screen.content = Text(
                        value='Error! Enter the numbers',
                        color='red',
                        size=16
                    )
                        page.update()
                        sleep(1)
                        display_screen.content = column_content
                        page.update()
                        return 

                    if bank_account['balance'] == 0 or bank_account['balance'] < int(text.value):
                        display_screen.content = text_error_balance
                        page.update()
                        sleep(1)
                        display_screen.content = column_content
                        page.update()
                    else:
                        bank_account['balance'] -= int(text.value)
                        bank_account['last_operations'].append(-int(text.value))
                        show_billets()

                elif current_mode.value == MODES['2']:
                    if text.value == '':
                        display_screen.content = Text(
                        value='Error! Enter the numbers',
                        color='red',
                        size=16
                    )
                        page.update()
                        sleep(1)
                        display_screen.content = column_content
                        page.update()
                        return 

                    bank_account['balance'] += int(text.value)
                    bank_account['balances_entered'].append(int(text.value))
                    bank_account['last_operations'].append(int(text.value))
                    extract_money()

                elif current_mode.value == MODES['3']:
                    for button_number in container_numbers.content.controls: button_number.disabled = False

                    display_screen.content = Row(
                        alignment=MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            Column(

                                controls=[
                                    Text(
                                        value='Current balance',
                                        size=16,
                                        color='black',
                                    ),
                                    Text(
                                        value=bank_account['balance'], 
                                        color=Colors.GREEN_600, 
                                        size=17
                                    )
                                ]
                            ),

                            Column(
                                scroll=True,
                                alignment=MainAxisAlignment.START,
                                controls=[
                                    Text(
                                        value='Incomes',
                                        size=16,
                                        color='black',
                                    ),
                                     Column([Text(value=option, size=17, color=Colors.GREEN_600) for option in bank_account['balances_entered'][::-1] 
                                        ]
                                    )

                                ]
                            ),
                            Column(
                                scroll=True,
                                controls=[
                                    Text(
                                        value='Last operations',
                                        size=16,
                                        color='black',
                                    ),
                                    Column(
                                        controls=[Text(value=option, size=17,color= 'red' if option < 0 else Colors.GREEN_600) for option in bank_account['last_operations'][::-1] ])

                                ]
                            )
                        ]
                    )
                    page.update()
                    
        def active_mode(e):
            nonlocal current_mode
            
            current_mode.value = e.control.text
            page.update()

            if current_mode.value == MODES['1']:
                container_modes.content.controls[1].disabled = True
                container_modes.content.controls[2].disabled = True
                page.update()

            elif current_mode.value == MODES['2']:
                container_modes.content.controls[0].disabled = True
                container_modes.content.controls[2].disabled = True
                page.update()

            elif current_mode.value == MODES['3']:
                container_modes.content.controls[0].disabled = True
                container_modes.content.controls[1].disabled = True
                page.update()

        MODES = {
            '1': 'Extract money',
            '2': 'Enter money',
            '3': 'Account status'    
        }

        bank_account = {
            'balance': 0,
            'balances_entered': [],
            'last_operations': []
        }       

        text = Text(
            value='',
            color=Colors.BLACK,
            weight=FontWeight.BOLD,
            size=18
        )
        
        text_error_balance = Text(
            value='Error! Your balance is insufficient',
            color=Colors.RED_600,
            size=17,
            weight=FontWeight.BOLD
        )

        text_error = Text(
            value='mistake! An operation cannot be executed if you did not select a mode or you started with 0 zeros',
            color=Colors.RED_600,
            size=17,
            weight=FontWeight.BOLD
        )

        text_welcome = Text(
            value='Welcome ATM',
            color='black',
            weight=FontWeight.BOLD,
            size=17
        )

        current_mode = Text(value='', size=15, color='black', weight=FontWeight.BOLD)

        column_content = Column(
            controls=[
                current_mode,
                text
            ]
        )

        display_screen = Container(
            width=650,
            height=160,
            bgcolor=Colors.LIGHT_GREEN_ACCENT_200,
            border_radius=10,
            padding=5,
            border=border.all(3, 'black'),
            content=column_content,
            data=1
        )

        container_numbers = Container(
            width=300,
            height=300,
            alignment=alignment.center,
            content=Row(
                wrap=True,  
                controls=[
                   Button(on_click=write_numbers_at_screen, height=45,text='1', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='2', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='3', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='4', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='5', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='6', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='7', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='8', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='9', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='0', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='00', width=90, color='white', bgcolor=Colors.GREY_600),
                   Button(on_click=write_numbers_at_screen, height=45,text='000', width=90, color='white', bgcolor=Colors.GREY_600)
                ]
            )
        )

        container_operations = Container(
            width=300,
            height=300,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                   Button(on_click=clear_screen, height=45,text='CLEAR', width=200, color=Colors.AMBER_500, bgcolor=Colors.GREY_600),
                   Button(on_click=execute_operation, height=45,text='CONFIRM', width=200, color=Colors.GREEN_400, bgcolor=Colors.GREY_600),
                   Button(on_click=turn_off, height=45,text='OFF', width=200, color=Colors.RED_400, bgcolor=Colors.GREY_600),
                   Button(on_click=cancel_operation ,height=45,text='CANCEL', width=200, color=Colors.RED_400, bgcolor=Colors.GREY_600),
                ]
            )
        )

        container_extraction_and_outlet_accessory = Container(
            width=300,
            height=190,
            content=Stack(
                controls=[
                    Container(
                        width=200,
                        height=30,
                        bgcolor=Colors.GREY_900,
                        alignment=alignment.center,
                        content=Container(
                            width=150,
                            height=2,
                            bgcolor=Colors.WHITE54
                        ),
                        border_radius=5,
                        top=5,
                        left=(300 - 200) / 2
                    ),
                    #base
                    Container(
                        width=220,
                        height=120,
                        bgcolor=Colors.GREY_600,
                        border_radius=10, 
                        left=(300 - 220) / 2,
                        top=60                   
                    )
                ]
            )
        ) 

        container_modes = Container(
            width=300,
            height=190,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Button(on_click=active_mode, height=45,text='Extract money', width=150, color='WHITE', bgcolor=Colors.GREY_600),
                    Button(on_click=active_mode, height=45,text='Enter money', width=150, color='WHITE', bgcolor=Colors.GREY_600),
                    Button(on_click=active_mode, height=45,text='Account status', width=150, color='WHITE', bgcolor=Colors.GREY_600),
                ]
            )
        )

        sub_container = Container(
            width=650,
            height=500,
            alignment=alignment.top_center,
            content=Row(
                alignment=MainAxisAlignment.SPACE_AROUND,
                controls=[
                        Column(
                            controls=[
                                container_numbers,
                                container_modes                    
                            ]
                        ),
                        Column(
                            controls=[
                                container_operations,
                                container_extraction_and_outlet_accessory
                            ]
                        )

                    ] 
                )
            )   

        container_machine = Container(
            width=680,
            height=700,
            bgcolor=Colors.GREY_800,
            padding=10,
            border_radius=border_radius.only(top_left=10, top_right=10),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.SPACE_AROUND,
                controls=[
                    display_screen,
                    sub_container
                ]
            )
        )
        container = Container(
            expand=True,
            alignment=alignment.center,
            content=container_machine
        )
        page.add(container)

app(main)