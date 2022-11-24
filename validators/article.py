from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    subject = StringField(name='subject',
                          validators=[DataRequired()])
    content = TextAreaField(name='content',
                            validators=[DataRequired()])
    thumb = FileField()
    submit = SubmitField()

class EditPostForm(FlaskForm):
    subject = StringField(name='subject' , 
    validators=[DataRequired('Subject Field is Required')])

    thumb = FileField()

    submit = SubmitField('Update Article')