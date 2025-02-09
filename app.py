from flask import Flask
from historical.Overlap.BBhistorical import BollingerBands

app = Flask(__name__)

@app.route('/bb', methods=['GET'])
def bollinger_band():
    model = BollingerBands()
    return model.generate_chart()

if __name__ == '__main__':
    app.run(port=5328)
