from flask import Flask, request
from historical.Momentum.ADXhistorical import AverageDirectionalMovement
from historical.Momentum.BOPhistorical import BalanceOfPower
from historical.Momentum.MACDhistorical import MovingAverageCD
from historical.Momentum.MOMhistorical import Momentum
from historical.Momentum.RSIhistorical import RelativeStrengthIndex
from historical.Momentum.STOCHF import StochasticFast
from historical.Momentum.ULTOSChistorical import UltimateOscillator
from historical.Overlap.BBhistorical import BollingerBands
from historical.Overlap.DEMAhistorical import DoubleExponentialMovingAverage
from historical.Overlap.FAMAhistorical import MESAAdaptiveMovingAverage
from historical.Overlap.KAMAhistorical import KaufmanAdaptiveMovingAverage
from historical.Overlap.SARhistorical import ParabolicSAR
from historical.Overlap.SMAhistorical import SimpleMovingAvg
from historical.PatternRecog.ENGhistorical import ENG
from historical.PatternRecog.HAMhistorical import HAM
from historical.PatternRecog.LADhistorical import LAD
from historical.PatternRecog.MShistorical import MS
from historical.PatternRecog.PPhistorical import PP
from historical.PatternRecog.TWShistorical import TWS
from historical.PatternRecog.UTRhistorical import UTR

app = Flask(__name__)

@app.route('/bb', methods=['GET'])
def bollinger_band():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = BollingerBands(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/sar', methods=['GET'])
def parabolic_sar():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = ParabolicSAR(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/sma', methods=['GET'])
def simple_moving_avg():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = SimpleMovingAvg(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/fama', methods=['GET'])
def MESA_adaptive_moving_avg():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = MESAAdaptiveMovingAverage(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/kama', methods=['GET'])
def kaufman_adaptive_moving_avg():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = KaufmanAdaptiveMovingAverage(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/dema', methods=['GET'])
def double_exp_moving_avg():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = DoubleExponentialMovingAverage(symbol=symbol, start=start, end=end)
    return model.generate_chart()

## Pattern recog

@app.route('/eng', methods=['GET'])
def eng():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = ENG(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/ham', methods=['GET'])
def ham():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = HAM(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/lad', methods=['GET'])
def lad():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = LAD(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/ms', methods=['GET'])
def ms():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = MS(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/pp', methods=['GET'])
def pp():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = PP(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/tws', methods=['GET'])
def tws():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = TWS(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/utr', methods=['GET'])
def utr():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = UTR(symbol=symbol, start=start, end=end)
    return model.generate_chart()

## Momentum

@app.route('/adx', methods=['GET'])
def adx():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = AverageDirectionalMovement(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/bop', methods=['GET'])
def bop():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = BalanceOfPower(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/mac', methods=['GET'])
def mac():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = MovingAverageCD(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/mom', methods=['GET'])
def mom():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = Momentum(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/rsi', methods=['GET'])
def rsi():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = RelativeStrengthIndex(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/stocf', methods=['GET'])
def stocf():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = StochasticFast(symbol=symbol, start=start, end=end)
    return model.generate_chart()

@app.route('/ultos', methods=['GET'])
def ultos():
    symbol = request.args.get("symbol")
    start = request.args.get("start")
    end = request.args.get("end")
    model = UltimateOscillator(symbol=symbol, start=start, end=end)
    return model.generate_chart()

if __name__ == '__main__':
    app.run(port=5328)
