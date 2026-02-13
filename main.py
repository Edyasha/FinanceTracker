from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup

from database import TransactionDB

Config.set("graphics", "width", 420)
Config.set("graphics", "height", 880)

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ми кажемо програмі: "Як тільки з'явиться перша вільна мілісекунда — завантаж дані"
        Clock.schedule_once(self.deferred_load)

    def deferred_load(self, dt):
        self.load_data()

    def save_data(self):
        raw_data = self.ids.amount_input.text.strip().replace(" ", "")
        popup = Popup(title="Застереження",
                      content=Label(text="Поле не має бути пустим, \nта містити від'ємні числа!"),
                      size_hint=(None, None), size=(300, 200), auto_dismiss=True)
        if raw_data == "":
            popup.open()
        elif raw_data and raw_data[0] == "-":
            popup.open()
            self.ids.amount_input.text = ""
        else:
            try:
                amount = float(raw_data)

                if self.ids.chk_income.active:
                    transaction_type = "Дохід"
                else:
                    transaction_type = "Витрата"

                app = App.get_running_app()
                app.db.add_transaction(amount, transaction_type)
                self.ids.amount_input.text = ""
                self.load_data()

            except ValueError:
                self.ids.amount_input.text = ""

    def load_data(self):
        app = App.get_running_app()
        records = app.db.get_all_transactions()
        income, expense = app.db.get_monthly_stats()

        self.ids.monthly_income.text = f"{income:,} грн."
        self.ids.monthly_expense.text = f"{expense:,} грн."

        self.ids.container.clear_widgets()

        for record in records:
            amount, date, t_type = record

            lbl_date = Label(text=str(date), color=(100,100,100,1))
            lbl_type = Label(text=str(t_type), color=(100,100,100,1))
            color = (0,0.6,0,1) if t_type == "Дохід" else (0.8,0,0,1)
            lbl_amount = Label(text=str(amount), color=color)

            self.ids.container.add_widget(lbl_date)
            self.ids.container.add_widget(lbl_type)
            self.ids.container.add_widget(lbl_amount)

class FinanceApp(App):
    db: TransactionDB
    def build(self):
        self.db = TransactionDB()
        return MainScreen()

if __name__ == '__main__':
    FinanceApp().run()