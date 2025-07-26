from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, IPAddress

class FirstRunForm(FlaskForm):
    ssid = StringField('WiFi Name (SSID)', validators=[DataRequired(), Length(min=2, max=32)])
    password = PasswordField('WiFi Password', validators=[DataRequired(), Length(min=8, max=64)])
    dhcp_start = StringField('Starting IP', validators=[DataRequired(), IPAddress()])
    dhcp_end = StringField('Ending IP', validators=[DataRequired(), IPAddress()])
    max_clients = IntegerField('Max Clients', default=32)
    admin_password = PasswordField('New Admin Password', validators=[DataRequired(), Length(min=8)])