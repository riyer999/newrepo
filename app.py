from flask import Flask, render_template, send_file
import pickle
import matplotlib

matplotlib.use('Agg')  # Set to non-GUI backend
import matplotlib.pyplot as plt
import tempfile

app = Flask(__name__, template_folder='templates')

# Load data from the pickle file
with open('allData.pkl', 'rb') as file:
    allData = pickle.load(file)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<ticker>')
def get_data(ticker):
    if ticker in allData:
        income_statement = allData[ticker]['income_statement']

        if 'Operating Expense' in income_statement.index:
            try:
                operating_expenses = income_statement.loc['Operating Expense']
                cleaned_expenses = operating_expenses[operating_expenses != 0].dropna()
                expenses_list = cleaned_expenses.values.tolist()
                dates = cleaned_expenses.index.astype(str).tolist()

                plt.figure(figsize=(10, 5))
                plt.bar(dates, expenses_list, color='blue', width=0.4)
                plt.title(f'Operating Expenses for {ticker}')
                plt.xlabel('Dates')
                plt.ylabel('Operating Expenses')
                plt.xticks(rotation=45)
                plt.tight_layout()

                plot_file = f'{ticker}_operating_expenses.png'
                plt.savefig(plot_file)
                plt.close()  # Clear the figure to free up memory

                return send_file(plot_file, mimetype='image/png')
            except Exception as e:
                return f'Error generating plot: {str(e)}', 500
        else:
            return f'Operating Expenses not found for ticker {ticker}.', 404
    else:
        return f'Ticker "{ticker}" not found in the data.', 404


if __name__ == '__main__':
    app.run(debug=True)
