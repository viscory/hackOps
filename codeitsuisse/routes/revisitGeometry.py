import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def driver():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = revisitGeometry(data.get('lineCoordinates'), data.get('shapeCoordinates'))
    # print(result)
    # logging.info("My result :{}".format(result))
    return result;




def determinant(p1, p2):
    return p1[0] * p2[1] - p1[1] * p2[0]

def itIntersects(q1, q2, p1, p2):
    xdiff = (q1[0] - q2[0], p1[0] - p2[0])
    ydiff = (q1[1] - q2[1], p1[1] - p2[1])

    div = determinant(xdiff, ydiff)
    if div == 0:
        return None

    d = (determinant(q1, q2), determinant(p1, p2))
    x = determinant(d, xdiff) / div
    y = determinant(d, ydiff) / div

    if (p1[0] <= x <= p2[0] or p2[0] <= x <= p1[0]) and (p1[1] <= y <= p2[1] or p2[1] <= y <= p1[1]):
        return x, y


def revisitGeometry(lineCoord, shapeCoord):
    lst = []
    p1 = lineCoord[0]["x"], lineCoord[0]["y"]
    p2 = lineCoord[1]["x"], lineCoord[1]["y"]
    q1 = shapeCoord[0]["x"], shapeCoord[0]["y"]
    firstpt = q1
    for i in range(len(shapeCoord) - 1):
        q2 = shapeCoord[i + 1]["x"], shapeCoord[i + 1]["y"]
        pt = itIntersects(p1, p2, q1, q2)
        if pt:
            lst.append({"x": round(pt[0], 2), "y": round(pt[1], 2)})
        q1 = q2
    pt = itIntersects(p1, p2, firstpt, q2)
    if pt:
        lst.append({"x": round(pt[0], 2), "y": round(pt[1], 2)})
    return json.dumps(lst)


if __name__ == "__main__":
    shape = [
        {"x": 21, "y": 70},
        {"x": 72, "y": 70},
        {"x": 72, "y": 127}
    ]
    line = [
        {"x": -58, "y": 56},
        {"x": -28, "y": 68}
    ]
    print("ANS", revisitGeometry(line, shape))
    shape = [
        {"x": -21, "y": -18},
        {"x": 71, "y": -18},
        {"x": 71, "y": 71},
        {"x": -21, "y": 71}
    ]
    line = [
        {"x": 68, "y": -8},
        {"x": 108, "y": 42}
    ]
    print("ANS", revisitGeometry(line, shape))
    shape = [
        {
            "x": 63,
            "y": 26
         },
        {
            "x": 115,
            "y": 26
         },
        {
            "x": 115,
            "y": 54
         },
        {
            "x": 63,
            "y": 54
         }
      ]
    line = [
        {
            "x": -88,
            "y": 85
         },
        {
            "x": -58,
            "y": 97
         }
      ]
    print("ANS", revisitGeometry(line, shape))
