import dash_mantine_components as dmc
from dash_iconify import DashIconify

def notification_update_show(id='',text='',title=''):
        return dmc.Notification(
            id=id,
            title=title,
            message=[text],
            disallowClose=False,
            #radius="xl",
            icon=[DashIconify(icon="feather:database", width=128)],
            action="show",
        )