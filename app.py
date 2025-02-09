from flask import Flask, request
from historical.Overlap.BBhistorical import BollingerBands

app = Flask(__name__)

@app.route('/bb', methods=['GET'])
def bollinger_band():
    symbol = request.args.get("symbol")
    smaTime = request.args.get("smaTime")
    model = BollingerBands(symbol=symbol, smaTime=smaTime)
    return model.generate_chart()

if __name__ == '__main__':
    app.run(port=5328)
