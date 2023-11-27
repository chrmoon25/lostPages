

# def onAppStart(app):
#     app.level = 5

# def drawFractal(level, cx, cy, r):
#     def drawMonkey(cx, cy, r):
#         tanCircle_r = r/1.75
#         tanCircle_cy = cy+1/3*r
#         mouthLine_x1 = cx - tanCircle_r
#         mouthLine_x2 = cx + tanCircle_r
#         eye_r = r/3.5
#         eye_y = cy-2/5*r
#         eye_x1 = cx-tanCircle_r*3/4
#         eye_x2 = cx+tanCircle_r*3/4
#         pupil_r = eye_r/1.75
#         highlights_r = pupil_r/2
#         highlights_x1 = eye_x1-pupil_r*2/4
#         highlights_x2 = eye_x2-pupil_r*2/4
#         highlights_y = eye_y-2/5*pupil_r
#         nose_r = eye_r/4
#         nose_x1 = cx - tanCircle_r/5
#         nose_x2 = cx + tanCircle_r/5
#         nose_y = tanCircle_cy-tanCircle_r/2

#         drawCircle(cx, cy, r, fill='saddlebrown', border='black', borderWidth = 3)
#         drawCircle(cx, tanCircle_cy, tanCircle_r, fill='tan', border='black', borderWidth = 3)

#         drawCircle(eye_x1, eye_y, eye_r, fill='white', border='black', borderWidth = 3)
#         drawCircle(eye_x2, eye_y, eye_r, fill='white', border='black', borderWidth = 3)

#         drawCircle(eye_x1, eye_y, pupil_r, fill='black', border='black', borderWidth = 3)
#         drawCircle(eye_x2, eye_y, pupil_r, fill='black', border='black', borderWidth = 3)

#         drawCircle(highlights_x1, highlights_y, highlights_r, fill='white')
#         drawCircle(highlights_x2, highlights_y, highlights_r, fill='white')

#         drawCircle(nose_x1, nose_y, nose_r, fill='black')
#         drawCircle(nose_x2, nose_y, nose_r, fill='black')

#         drawLine(mouthLine_x1, tanCircle_cy, mouthLine_x2, tanCircle_cy, lineWidth = 3)

#     if level == 0:
#         drawMonkey(cx, cy, r)
#     else: 
#         drawMonkey(cx, cy, r)
#         newR = r/2
#         drawFractal(level-1, (cx-r*2/3)-newR, cy-2/3*r, newR)
#         drawFractal(level-1, (cx+r*2/3)+newR, cy-2/3*r, newR)

# def onKeyPress(app, key):
#     if (key in ['up', 'right']) and (app.level < 5):
#         app.level += 1
#     elif (key in ['down', 'left']) and (app.level > 0):
#         app.level -= 1

# def redrawAll(app):
#     drawFractal(app.level, app.width/2, app.height/2 + 30, 150)
#     drawLabel('Use the arrow keys to change the level!',
#             app.width/2, 50, size=12, bold=True)

# def main():
#     runApp()

# main()


