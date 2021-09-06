from kary_sketch import KAry_Sketch
from scapy.all import copy

def MA(sketch_list,w):
    """Uses the Moving Average Model to build the forecast sketch from the list of sketches observed in the past

    Parameters
    ----------
    sketch_list : list
        A list of observed sketches
    w : int
        number of past sketches saved for forecast

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(sketch_list[0].sketch)
    width = len(sketch_list[0].sketch[0])
    new_forecast_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
        for j in range(0,width):
            _sum = 0
            for p in range(2,w+2):
                _sum = _sum + sketch_list[-p].sketch[i][j]
            new_forecast_sketch.sketch[i][j] = _sum / w
    return new_forecast_sketch

def SMA(sketch_list,w,weigths):
    """Uses the S-shaped Moving Average Model to build the forecast sketch from the list of sketches observed in the past

    Parameters
    ----------
    sketch_list : list
        A list of observed sketches
    w : int
        The number of past sketches saved for forecast
    weigths: list
        A list of weights given to each past epoch

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(sketch_list[0].sketch)
    width = len(sketch_list[0].sketch[0])
    new_forecast_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
        for j in range(0,width):
            _sum = 0
            for p in range(2,w+2):
                _sum = _sum + (weigths[p-2] * sketch_list[-p].sketch[i][j])
            new_forecast_sketch.sketch[i][j] = _sum / sum(weigths)
    return new_forecast_sketch

def EWMA(previous_forecast_sketch,previous_observed_sketch,alpha):
    """Uses the Exponentially Weighted Moving Average Model to build the forecast sketch from the previous forecast and observed sketch

    Parameters
    ----------
    previous_forecast_sketch : KAry_Sketch
        A forecast sketch
    previous_observed_sketch : KAry_Sketch
        An observed sketch
    alpha : float
        The alpha value to be used by the EWMA

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(previous_observed_sketch.sketch)
    width = len(previous_observed_sketch.sketch[0])
    new_forecast_sketch = KAry_Sketch(depth,width)
    if previous_forecast_sketch != None:
        for i in range(0,depth):
            for j in range(0,width):
                new_forecast_sketch.sketch[i][j] = (alpha*previous_observed_sketch.sketch[i][j]) + ((1-alpha)*previous_forecast_sketch.sketch[i][j])
        return new_forecast_sketch
    else:
        return copy.deepcopy(previous_observed_sketch)

def EWMA_approx(previous_forecast_sketch,previous_observed_sketch,alpha):
    """Uses the Exponentially Weighted Moving Average Model with bit-shifts to build the forecast sketch from the previous forecast and observed sketch

    Parameters
    ----------
    previous_forecast_sketch : KAry_Sketch
        A forecast sketch
    previous_observed_sketch : KAry_Sketch
        An observed sketch
    alpha : float
        The alpha value to be used by the EWMA

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(previous_observed_sketch.sketch)
    width = len(previous_observed_sketch.sketch[0])
    new_forecast_sketch = KAry_Sketch(depth,width)
    if previous_forecast_sketch != None:
        for i in range(0,depth):
            for j in range(0,width):
                observed = 0
                forecast = 0
                if alpha == 0.125:
                    observed = int(previous_observed_sketch.sketch[i][j] >> 3)
                    forecast = int(previous_forecast_sketch.sketch[i][j] >> 1) + int(previous_forecast_sketch.sketch[i][j] >> 2) + int(previous_forecast_sketch.sketch[i][j] >> 3)
                elif alpha == 0.25:
                    observed = int(previous_observed_sketch.sketch[i][j] >> 2)
                    forecast = int(previous_forecast_sketch.sketch[i][j] >> 1) + int(previous_forecast_sketch.sketch[i][j] >> 2)
                elif alpha == 0.375:
                    observed = int(previous_observed_sketch.sketch[i][j] >> 2) + int(previous_observed_sketch.sketch[i][j] >> 3)
                    forecast = int(previous_forecast_sketch.sketch[i][j] >> 1) + int(previous_forecast_sketch.sketch[i][j] >> 3)
                elif alpha == 0.5:
                    observed = int(previous_observed_sketch.sketch[i][j] >> 1)
                    forecast = int(previous_forecast_sketch.sketch[i][j] >> 1)
                elif alpha == 0.625:
                    observed = int(previous_observed_sketch.sketch[i][j] >> 1) + int(previous_observed_sketch.sketch[i][j] >> 3)
                    forecast = int(previous_forecast_sketch.sketch[i][j] >> 2) + int(previous_forecast_sketch.sketch[i][j] >> 3)
                elif alpha == 0.75:
                    observed = int(previous_observed_sketch.sketch[i][j] >> 1) + int(previous_observed_sketch.sketch[i][j] >> 2)
                    forecast = int(previous_forecast_sketch.sketch[i][j] >> 2)
                elif alpha == 0.875:
                    observed = int(previous_observed_sketch.sketch[i][j] >> 1) + int(previous_observed_sketch.sketch[i][j] >> 2) + int(previous_observed_sketch.sketch[i][j] >> 3)
                    forecast = int(previous_forecast_sketch.sketch[i][j] >> 3)

                new_forecast_sketch.sketch[i][j] = observed + forecast
        return new_forecast_sketch
    else:
        return copy.deepcopy(previous_observed_sketch)

def NSHW(previous_forecast_sketch,previous_observed_sketch,observed_sketch,previous_trend,previous_smoothing,alpha,beta):
    """Uses the Non-Seasonal Holt-Winters Model to build the forecast sketch from the previous forecast, observed sketch, trend and smoothing

    Parameters
    ----------
    previous_forecast_sketch : KAry_Sketch
        A forecast sketch
    previous_observed_sketch : KAry_Sketch
        An observed sketch
    observed_sketch : KAry_Sketch
        An observed sketch
    previous_trend : KAry_Sketch
        The previous trend sketch
    previous_smoothing : KAry_Sketch
        The previous smoothing sketch
    alpha : float
        The alpha value to be used by the NSHW
    beta : float
        The beta value to be used by the NSHW

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    KAry_Sketch
        The smoothing sketch
    KAry_Sketch
        The trend sketch
    """

    depth = len(previous_observed_sketch.sketch)
    width = len(previous_observed_sketch.sketch[0])
    smoothing_sketch = KAry_Sketch(depth,width)
    trend_sketch = KAry_Sketch(depth,width)

    #smoothing
    if previous_forecast_sketch != None:
        for i in range(0,depth):
            for j in range(0,width):
                smoothing_sketch.sketch[i][j] = (alpha*previous_observed_sketch.sketch[i][j]) + ((1-alpha)*previous_forecast_sketch.sketch[i][j])
    else:
        smoothing_sketch = copy.deepcopy(previous_observed_sketch)

    #trend
    if previous_forecast_sketch != None:
        for i in range(0,depth):
            for j in range(0,width):
                trend_sketch.sketch[i][j] = (beta*(smoothing_sketch.sketch[i][j] - previous_smoothing.sketch[i][j])) + ((1-beta)*previous_trend.sketch[i][j])
    else:
        for i in range(0,depth):
            for j in range(0,width):
                trend_sketch.sketch[i][j] = observed_sketch.sketch[i][j] - previous_observed_sketch.sketch[i][j]

    #Forecasting sketch

    forecasting_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
            for j in range(0,width):
                forecasting_sketch.sketch[i][j] = trend_sketch.sketch[i][j] + smoothing_sketch.sketch[i][j]

    return forecasting_sketch, smoothing_sketch, trend_sketch
