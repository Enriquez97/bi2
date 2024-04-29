import dash_mantine_components as dmc
from dash_iconify import DashIconify



def menu_avatar(avatar_user = "",name_user = "Edwardo Enriquez"):
    return  \
    dmc.Menu(
        [
            dmc.MenuTarget(
            [
                dmc.Avatar(
                    src = avatar_user,
                    size ="md",
                    radius="xl",
                    mr=10,
                    style={"display": "inline-block", "vertical-align": "middle"}
                                        
                ),
                dmc.Text(name_user, size="sm", weight=600,mr=20,style={"display": "inline-block", "vertical-align": "middle"}),
                
                                
            ]
            ),
            dmc.MenuDropdown(
                [
                    dmc.MenuLabel("Application"),
                        dmc.MenuItem("Settings", icon=DashIconify(icon="tabler:settings")),
                        #dmc.MenuItem("Messages", icon=DashIconify(icon="tabler:message")),
                        #dmc.MenuItem("Gallery", icon=DashIconify(icon="tabler:photo")),
                        #dmc.MenuItem("Search", icon=DashIconify(icon="tabler:search")),
                        #dmc.MenuDivider(),
                        #dmc.MenuLabel("Danger Zone"),
                        #dmc.MenuItem(
                        #    "Transfer my data",
                        #    icon=DashIconify(icon="tabler:arrows-left-right"),
                        #),
                        dmc.MenuItem(
                            "Logout",
                            icon=DashIconify(icon="tabler:logout"),
                            href="/logout",
                            refresh = True
                            
                            
                            #color="red",
                        ),
                ]
            ),
        ],
        trigger="hover"
    ) 