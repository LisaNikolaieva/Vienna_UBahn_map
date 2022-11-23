from matplotlib import pyplot as plt
import pandas as pd
import shapefile as shp

import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask

plt.rcParams["figure.autolayout"] = True
app = Flask(__name__)


def get_subway_color(subway_line):
    u2col = {
        "U1": '#ff0000',
        "U2": '#8000ff',
        "U3": '#ff8000',
        "U4": '#009d00',
        "U6": '#A0522D'
    }

    col = '#540CF2'  # default

    if subway_line in u2col:
        col = u2col[subway_line]

    return col


@app.route('/<subway_line>')            #all_lines U1 U2 U3 U4 U6
def plot_tube_line(subway_line):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    sf = shp.Reader("./data/vienna/BEZIRKSGRENZEOGDPolygon.shp", encoding="latin1")

    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        axis.plot(x, y, '-', color='#aaaaaa')

    csv_file = "./data/OEFFLINIENOGD.csv"
    df = pd.read_csv(csv_file, sep=',')
    UBahn = []

    if subway_line == 'all_lines':
        UBahn = df[df.LTYPTXT == 'U-Bahn'].LBEZEICHNUNG.unique()
    else:
        UBahn.append(subway_line)

    for subway_line in UBahn:
        df1 = df[df.LBEZEICHNUNG == subway_line]
        a = df1.SHAPE.tolist()
        b = []
        for i in a:
            b.append(i[12:-1])
        for j in b:
            x = []
            y = []
            r2 = j.split(',')
            for i in r2:
                r3 = i.strip().split(' ')
                x.append(float(r3[0]))
                y.append(float(r3[1]))
            axis.plot(x, y, get_subway_color(subway_line))

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run()
