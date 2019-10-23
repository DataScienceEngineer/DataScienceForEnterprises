import dash
import flask
server = flask.Flask(__name__,static_url_path='/')
app = dash.Dash(server=server)
#server = app.server
app.config.supress_callback_exceptions = True

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})