from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from database import TransactionDB

Config.set("graphics", "width", 420)
Config.set("graphics", "height", 880)

class MainScreen(BoxLayout):
    def save_data(self):
        raw_data = self.ids.amount_input.text.strip().replace(" ", "")

        try:
            amount = float(raw_data)

            if self.ids.chk_income.active:
                transaction_type = "Дохід"
            else:
                transaction_type = "Витрата"

            app = App.get_running_app()
            app.db.add_transaction(amount, transaction_type)

            print(f"Сума: {amount} збережена!")
            print(self.ids.chk_income.active)
            self.ids.amount_input.text = ""

        except ValueError:
            print("Помилка! Введіть будь ласка число!")

    def load_data(self):
        app = App.get_running_app()
        records = app.db.get_all_transactions()

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

        print(app.db.get_monthly_stats())

class FinanceApp(App):
    db: TransactionDB
    def build(self):
        self.db = TransactionDB()
        return MainScreen()

if __name__ == '__main__':
    FinanceApp().run()