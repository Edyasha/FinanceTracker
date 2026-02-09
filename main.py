from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from database import TransactionDB

class MainScreen(BoxLayout):
    def save_data(self):
        raw_data = self.ids.amount_input.text.strip().replace(" ", "")

        try:
            amount = float(raw_data)
            app = App.get_running_app()
            app.db.add_transaction(amount, "Витрата")

            print(f"Сума: {amount} збережена!")
            self.ids.amount_input.text = ""

        except ValueError:
            print("Помилка! Введіть будь ласка число!")

    def load_data(self):
        app = App.get_running_app()
        records = app.db.get_all_transactions()

        print("--- Ваші записи ---")
        for record in records:
            amount, date, t_type = record
            print(f"[{date}] {t_type}: {amount}")
            print("--------------------")

class FinanceApp(App):
    db: TransactionDB
    def build(self):
        self.db = TransactionDB()
        return MainScreen()

if __name__ == '__main__':
    FinanceApp().run()