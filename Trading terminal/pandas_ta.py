import pandas as pd


def crossunder(source1, source2):
    data1 = source1 - source2
    data2 = data1.shift()
    result = (data1 < 0) & (data2 > 0)
    return result


def crossover(source1, source2):
    data1 = source1 - source2
    data2 = data1.shift()
    result = (data1 > 0) & (data2 < 0)
    return result


def cross(source1, source2):
    data1 = source1 - source2
    data2 = data1.shift()
    result = ((data1 > 0) & (data2 < 0)) | ((data1 < 0) & (data2 > 0))
    return result


def pivotlow(source, leftbars, rightbars):
    result = pd.Series([None] * source.shape[0], source.index)
    min = source.rolling(leftbars + rightbars + 1).min()
    pivot = min[min == source.shift(rightbars)]
    result.loc[pivot.index] = pivot
    return result.astype(float)


def pivothigh(source, leftbars, rightbars):
    result = pd.Series([None] * source.shape[0], source.index)
    max = source.rolling(leftbars + rightbars + 1).max()
    pivot = max[max == source.shift(rightbars)]
    result.loc[pivot.index] = pivot
    return result.astype(float)


def lowest(source, length):
    result = source.fillna(0).rolling(length).min()
    return result


def highest(source, length):
    result = source.fillna(0).rolling(length).max()
    return result


def sma(source, length):
    result = source.rolling(length).mean()
    return result


def ema(source, length):
    data = source.copy()
    alpha = 2 / (length + 1)
    na = data.isna().sum()
    sma = data[na:length + na].mean()
    data[length + na - 1] = sma
    ema = pd.DataFrame.ewm(
        data[length + na - 1:], alpha=alpha, adjust=False
    ).mean()
    result = [None] * (length + na - 1)
    result.extend(ema)
    return pd.Series(result, source.index)


def rma(source, length):
    data = source.copy()
    alpha = 1 / length
    na = data.isna().sum()
    sma = data[na:length + na].mean()
    data[length + na - 1] = sma
    rma = pd.DataFrame.ewm(
        data[length + na - 1:], alpha=alpha, adjust=False
    ).mean()
    result = [None] * (length + na - 1)
    result.extend(rma)
    return pd.Series(result, source.index)


def tr(high, low, close, handle_na):
    hl = high - low
    hc = abs(high - close.shift())
    lc = abs(low - close.shift())
    if handle_na:
        hc[0] = abs(high[0] - close[0])
        lc[0] = abs(low[0] - close[0])
    df = pd.DataFrame([hl, hc, lc]).transpose()
    na = df.isna().sum().max()
    result = [None] * na
    result.extend(df.max(axis=1)[na:])
    return pd.Series(result, high.index)


def atr(high, low, close, length):
    true_range = tr(high, low, close, True)
    return rma(true_range, length)


def change(source, length=1):
    return source - source.shift(length)

