from wtforms import Form, validators
from wtforms.fields import simple


class RegForm(Form):
    user = simple.StringField(
        label='用户名',
        validators=[
            validators.Length(min=6, max=12, message='用户名长度为6~12'),
            validators.Regexp('^[\u4e00-\u9fa5_a-zA-Z0-9]+$', message='用户名只允许中文、英文、数字下划线组合')
        ],
    )

    nick = simple.StringField(
        label='昵称',
        validators=[
            validators.Length(max=8, message='昵称长度最长为8'),
            validators.Regexp('^[\u4e00-\u9fa5_a-zA-Z0-9]+$', message='昵称只允许中文、英文、数字下划线组合')
        ],
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.Length(min=8, max=16, message='密码长度为8~16'),
            validators.Regexp('^[_a-zA-Z0-9]+$', message='密码只允许英文、数字下划线组合')
        ],
    )

    re_pwd = simple.PasswordField(
        label='确认密码',
        validators=[
            validators.EqualTo(fieldname='pwd', message='两次密码输入不一致')
        ],
    )

    email = simple.StringField(
        label='邮箱',
        validators=[
            validators.Email(message='邮箱格式错误')
        ]
    )
