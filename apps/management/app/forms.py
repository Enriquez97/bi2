import pandas as pd
import dash_mantine_components as dmc
from datetime import datetime
from django_plotly_dash import DjangoDash
from dash_iconify import DashIconify
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.layouts.base import Content
from ...resource.helpers.make_grid import Grid,Col
from ..utils import valid_var_user, validar_contraseña
from ...resource.components.toggle import darkModeToggleDash
from ...management.crud.create import createProfile,createEmpresa,updateProfile
from ..api_net import ApisNetPe
from ...resource.utils.data import *

class DashFormUser:
    #def __init__(self, ip: str, token :str):
    #    self.ip = ip
    #    self.token = token
    def app_form_new_user(self, code: str, data_inputs : dict):#,data_login = {}
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
                #suppress_callback_exceptions=True
        )
        roles_ = [{'label': rol, 'value': id} for id,rol in data_inputs['roles']]
        empresas = [{'label': rol, 'value': id} for id,rol in data_inputs['empresas']] if len(data_inputs['empresas'])>0 else [data_inputs['empresa_']]
        modal_error = [dmc.Alert(children=[dmc.Text("Revisa si todos los elementos del formulario estan llenos o actualiza."),dmc.Space(h=30),dmc.Group([html.A(dmc.Button("Actualizar", id="btn-close-modal"),href="/user/create-user")],position="right")], title="Error!", color="red")]
        modal_success = [dmc.Alert(children=[dmc.Text("Se creo un usuario nuevo."),dmc.Space(h=30),dmc.Group([html.A(dmc.Button("Regresar", id="btn-close-modal"),href="/user/usuarios")],position="right")], title="Success!", color="green")]
        app.layout =  \
        Content([
            dmc.Modal(
                title="", 
                id="modal-alert", 
                zIndex=10000,
                closeOnClickOutside=False,
                closeOnEscape=False,
                
                centered=True,
                padding=0
            ),
            Grid([
                Col([
                    dmc.Title("Crear Usuario Nuevo")
                ],size=11),
                Col([
                    darkModeToggleDash(pl = 15,pt = 10)
                ],size=1),
                Col([
                    dmc.TextInput(label="Nombres:",placeholder="insertar", id = "name"),
                ],size=6),
                Col([
                    dmc.TextInput(label="Apellidos:",placeholder="insertar", id = "last_name"),
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Celular:",
                        placeholder="insertar",
                        icon=DashIconify(icon="bi:phone"),
                        id = "phone"
                    ),
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Email:",
                        placeholder="insertar",
                        icon=DashIconify(icon="ic:round-alternate-email"),
                        id = "email"
                    )
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Username:",
                        placeholder="",
                        icon=DashIconify(icon="bi:person"),
                        id = "username",
                        disabled=True
                    ),
                ],size=4),
                Col([
                    dmc.PasswordInput(
                        label="Contraseña:",
                        placeholder="insertar",
                        icon=DashIconify(icon="bi:shield-lock"),
                        id = "password"
                    )
                ],size=4),
                Col([
                    dmc.PasswordInput(
                        label="Ingrese Nuevamente Contraseña:",
                        placeholder="insertar",
                        icon=DashIconify(icon="bi:shield-lock"),
                        id = "password_confirm"
                    )
                ],size=4),
                Col([
                    dmc.Select(
                        label="Empresa",
                        placeholder="Select",
                        value = data_inputs['empresa_'],
                        data = empresas,
                        id = "empresa",
                        disabled = data_inputs['disabled_select']
                    ),
                ],size=6),
                Col([
                    dmc.Select(
                        label="Rol",
                        placeholder="Select",
                        value=roles_[-1]['value'],
                        data= roles_,
                        id = "rol",
                        clearable=False
                    ),
                ],size=6),
                Col([
                    dcc.Upload(dmc.Button("Upload Imagen",fullWidth=True,color="indigo"),id='upload-image')
                ],size = 3),
                Col([
                    dmc.Text(id ="output-image-upload",weight=500, children=["Inserte imagen"],align="left",mt=6)
                ],size = 9),
                Col([
                    dmc.Button("Guardar",fullWidth=True,id="btn-save")
                ],size=6),
                Col([
                    dcc.Link(dmc.Button(id = "btn-cancel",children="Cancelar",leftIcon=DashIconify(icon="fluent:backspace-20-filled"),fullWidth=True,color="red"), href="/user/usuarios", refresh=True),
                    
                ],size=6),
                Col([
                    html.Div(id="alert")
                ]),

            ])
        ],fluid=False)
        app.clientside_callback(
        """
        function(checked) {
                if (checked) {
                    return {"colorScheme": "light"};
                } else {
                    return {"colorScheme": "dark"};
                }
        }
        """,
        Output('themeHolder','theme'),Input('themeSwitch','checked'))

        app.clientside_callback(
            """
            function(content, name) {
                if (content) {
                    return name;
                } else {
                    return "Inserte imagen";
                }
            }
            """,
            Output('output-image-upload', 'children'),
            Input('upload-image', 'contents'),
            State('upload-image', 'filename')
        )    
        
        app.clientside_callback(
            """
            function validate_email(email) {
                if (email.includes("@") || email === "") {
                    return false;
                } else {
                    return "Incorrecto";
                }
            }
            """,
            Output('email', 'error'),
            [Input('email', 'value')]
        )
        app.clientside_callback(
            """
            function(name, last_name) {
                if (name.length > 3 && last_name.length > 3) {
                    var firstInitial = name.trim().toLowerCase()[0];
                    var firstLastName = last_name.trim().toLowerCase().split(' ')[0];
                    var datetimePart = new Date().getMilliseconds().toString();
                    var datetimeSeg = new Date().getSeconds().toString().substr(-1);
                    return firstInitial + firstLastName + datetimePart + datetimeSeg;
                } else {
                    return '';
                }
            }
            """,
            Output('username', 'value'),
            Input('name', 'value'),
            Input('last_name', 'value')
        )
        """
        @app.callback(Output('password', 'error'),Input('password', 'value'))
        def validad_password(password):
            if len(password)>0:
                value = validar_contraseña(password)
                if  value == True:
                    return False
                else:
                    return "Contraseña Inválida"    
        """
        app.clientside_callback(
            """
            function(password) {
                function validar_contraseña(password) {
                    // Reemplaza esta función con tu lógica de validación
                    const minLength = 8;
                    const hasUpperCase = /[A-Z]/.test(password);
                    const hasLowerCase = /[a-z]/.test(password);
                    const hasNumbers = /\d/.test(password);
                    const hasNonalphas = /\W/.test(password);
                    
                    return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasNonalphas;
                }

                if (password.length > 0) {
                    const isValid = validar_contraseña(password);
                    if (isValid) {
                        return false;
                    } else {
                        return "Contraseña Inválida";
                    }
                } else {
                    return '';
                }
            }
            """,
            Output('password', 'error'),
            Input('password', 'value')
        )
        
        app.clientside_callback(
            """
            function validate_password_confirm(password_confirm, password) {
                if (password_confirm === password) {
                    return false;
                } else {
                    return "Las contraseñas no coinciden";
                }
            }
            """,
            Output('password_confirm', 'error'),
            [Input('password_confirm', 'value'), Input('password', 'value')]
        )    
       
        @app.callback(Output('modal-alert', 'opened'),
                    Output('modal-alert', 'children'),
                    Output("modal-alert","withCloseButton"),
                    Input('btn-save', 'n_clicks',),#0
                    State('name', 'value'),#1
                    State('last_name', 'value'),#2
                    State('phone', 'value'),#3
                    State('email', 'value'),#4
                    State('username', 'value'),#5
                    State('password', 'value'),#6
                    State('password_confirm', 'value'),#7
                    State('empresa', 'value'),#8
                    State('rol', 'value'),#9
                    State('upload-image', 'filename'),#10
                    State('upload-image', 'contents'),#11
                    State('password', 'error'),#12
                    State("modal-alert", "opened"),#13
                    prevent_initial_call=True,
        )
        def update_output(*args):
            #modal-alert
            
            if args[0]:
                
                if valid_var_user(args[1:-2]) ==  "NICE":
                    
                    if args[-2] == False and args[6] == args[7] and args[4].__contains__("@") == True and  (args[5] !="" or args[5] != None ) and validar_contraseña(args[6]) == True and (args[3] !="" or args[3] != None ):#
                        createProfile(data=args[1:-2])
                        return not args[13], modal_success,False#dmc.Alert("AW", title="Success!", color="green")
                    else:
                        return not args[13], modal_error,False#dmc.Alert("error!", title="Danger!", color="red")
                else:
                    return not args[13], modal_error, False#dmc.Alert("error!", title="Danger!", color="red")
        
        return app
    
    def app_form_new_company(self, code: str,data_inputs:dict):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        rubros = [{'label': rol, 'value': id} for id,rol in data_inputs['rubros']]
        modal_error = [dmc.Alert(children=[dmc.Text("Revisa si todos los elementos del formulario estan llenos."),dmc.Space(h=30),dmc.Group([html.A(dmc.Button("Actualizar", id="btn-close-modal"),href="/user/create-empresa")],position="right")], title="Error!", color="red")]
        modal_success = [dmc.Alert(children=[dmc.Text("Se creo una empresa correctamente."),dmc.Space(h=30),dmc.Group([html.A(dmc.Button("Regresar", id="btn-close-modal"),href="/")],position="right")], title="Success!", color="green")]
        app.layout =  \
        Content([
            dmc.Modal(
                title="", 
                id="modal-alert", 
                zIndex=10000,
                closeOnClickOutside=False,
                closeOnEscape=False,
                
                centered=True,
                padding=0
            ),
            Grid([
                Col([
                    dmc.Title("Crear Empresa")
                ],size=11),
                Col([
                    darkModeToggleDash(pl = 15,pt = 10)
                ],size=1),
                Col([
                    dmc.TextInput(
                        label="RUC:",
                        placeholder="",
                        icon=DashIconify(icon="bi:search"),
                        id = "ruc"
                    ),
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Razón Social:",
                        placeholder="",
                        icon=DashIconify(icon="bi:building"),
                        id = "name_empresa",
                        disabled=False
                    )
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Telefono:",
                        placeholder="",
                        icon=DashIconify(icon="bi:telephone"),
                        id = "telefono"
                    ),
                ],size=6),
                Col([
                    dmc.Select(
                        label="Rubro",
                        placeholder="Select",
                        value=rubros[-1]['value'],
                        data=rubros,
                        id = "rubro"
                    ),
                ],size=6),
            ]),
            
            dmc.Divider(label="Conexión Api", labelPosition="center"),
            Grid([
                Col([
                    dmc.TextInput(
                        label="IP:",
                        placeholder="",
                        icon=DashIconify(icon="bi:person-check"),
                        id = "ip"
                    ),
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Token:",
                        placeholder="",
                        #icon=DashIconify(icon="bi:person-check"),
                        id = "token"
                    ),
                ],size=6),
            ]),
            dmc.Divider(label="Conexión Server SQL", labelPosition="center"),
            Grid([
                Col([
                    dmc.TextInput(
                        label="Server:",
                        placeholder="",
                        #icon=DashIconify(icon="bi:database"),
                        id = "server"
                    ),
                ],size = 6),
                Col([
                    dmc.TextInput(
                        label="Base de Datos:",
                        placeholder="",
                        icon=DashIconify(icon="bi:database"),
                        id = "bd"
                    ),
                ],size = 6),
                Col([
                    dmc.TextInput(
                        label="User BD:",
                        placeholder="",
                        icon=DashIconify(icon="bi:person-lock"),
                        id = "user_bd"
                    ),
                ],size = 6),
                
                Col([
                    dmc.PasswordInput(
                        label="Password BD:",
                        placeholder="",
                        icon=DashIconify(icon="bi:shield-lock"),
                        id = "password_bd"
                    )
                ],size = 6)
            ]),
            
            Grid([
                Col([
                    dcc.Upload(dmc.Button("Upload Imagen",fullWidth=True,color="indigo",mt=30),id='upload-image')
                ],size = 2),
                Col([
                    html.Div(id ="output-image-upload", style={"margin-top": 30})
                ],size = 4),
                Col([
                    dmc.Select(
                        label="Tipo de Conexión",
                        placeholder="Select",
                        value="Api",
                        data=["Api","Server Sql"],
                        clearable=False,
                        id = "tipo_conexion"
                    ),
                ],size = 6),
                Col([
                    dmc.Button("Guardar",fullWidth=True,id="btn-save")
                ],size=6),
                Col([
                    dcc.Link(dmc.Button(id = "btn-cancel",children="Cancelar",leftIcon=DashIconify(icon="fluent:backspace-20-filled"),fullWidth=True,color="red"), href="/user/usuarios", refresh=True)
                ],size=6),
                Col([
                    html.Div(id="alert")
                ]),
            ])
        ],fluid=False)
        app.clientside_callback(
        """
        function(checked) {
                if (checked) {
                    return {"colorScheme": "light"};
                } else {
                    return {"colorScheme": "dark"};
                }
        }
        """,
        Output('themeHolder','theme'),Input('themeSwitch','checked'))
        
        app.clientside_callback(
            """
            function(content, name) {
                if (content) {
                    return name;
                } else {
                    return "Inserte imagen";
                }
            }
            """,
            Output('output-image-upload', 'children'),
            Input('upload-image', 'contents'),
            State('upload-image', 'filename')
        )
        app.clientside_callback(
            """
            function(ruc) {
                if (ruc.length === 11 || ruc === "") {
                    return '';
                } else {
                    return 'El ruc debe tener 11 dígitos';
                }
            }
            """,
            Output('ruc', 'error'),
            Input('ruc', 'value')
        )
        @app.callback(
              Output('name_empresa', 'value'),
              Input('ruc', 'value'),
              )
        def update_completar_name_empresa(ruc):
            if  len(ruc) == 11:
                data_empresa = ApisNetPe().get_company(ruc = str(ruc))
                return data_empresa['razonSocial']
            else:
                return '' 
            
        @app.callback(Output('modal-alert', 'opened'),
                    Output('modal-alert', 'children'),
                    Output("modal-alert","withCloseButton"),
                    Input('btn-save', 'n_clicks',),#0
                    State('ruc', 'value'),#1
                    State('name_empresa', 'value'),#2
                    State('telefono', 'value'),#3
                    
                    State('rubro', 'value'),#4
                    State('ip', 'value'),#5
                    State('token', 'value'),#6
                    
                    State('server', 'value'),#7
                    State('bd', 'value'),#8
                    State('user_bd', 'value'),#9
                    State('password_bd', 'value'),#10
                    
                    State('upload-image', 'contents'),#11
                    State("tipo_conexion","value"),#12
                    State("modal-alert", "opened"),#13
                    prevent_initial_call=True,
        ) 
        def update_output(*args):
            if args[0]:
                print(args[1:-1])
                if valid_var_user(args[1:-1]) ==  "NICE":
                    if len(args[1]) == 11:
                        createEmpresa(args[1:-1])
                        return not args[13], modal_success,True
                    else:
                        return not args[13], modal_error,True
                else:
                    return not args[13], modal_error, True
        return app
    
    def app_form_mod_user(self, code: str, data_inputs : dict):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
                #suppress_callback_exceptions=True
        )
        imagen_avatar = data_inputs['image']
        roles_ = [{'label': rol, 'value': id} for id,rol in data_inputs['roles']]
    
        modal_error = [dmc.Alert(children=[dmc.Text("Revisa si todos los elementos del formulario estan llenos o actualiza."),dmc.Space(h=30),dmc.Group([html.A(dmc.Button("Actualizar", id="btn-close-modal"),href="/user/create-user")],position="right")], title="Error!", color="red")]
        modal_success = [dmc.Alert(children=[dmc.Text(f"Se Actualizaron los datos de {data_inputs['name_user']}"),dmc.Space(h=30),dmc.Group([html.A(dmc.Button("Regresar", id="btn-close-modal"),href="/user/usuarios")],position="right")], title="Success!", color="green")]
        app.layout =  \
        Content([
            dmc.Modal(
                title="", 
                id="modal-alert", 
                zIndex=10000,
                closeOnClickOutside=False,
                closeOnEscape=False,
                
                centered=True,
                padding=0
            ),
            Grid([
                Col([
                    dmc.Title(f"Modificar Usuario {data_inputs['name_user']}")
                ],size=11),
                Col([
                    darkModeToggleDash(pl = 15,pt = 10)
                ],size=1),
                Col([
                    dmc.TextInput(label="Nombres:",placeholder="insertar", id = "name", value=data_inputs['name_profile']),
                ],size=6),
                Col([
                    dmc.TextInput(label="Apellidos:",placeholder="insertar", id = "last_name",value=data_inputs['surname_profile']),
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Celular:",
                        placeholder="insertar",
                        icon=DashIconify(icon="bi:phone"),
                        id = "phone",
                        value=data_inputs['phone']
                    ),
                ],size=6),
                Col([
                    dmc.TextInput(
                        label="Email:",
                        placeholder="insertar",
                        icon=DashIconify(icon="ic:round-alternate-email"),
                        id = "email",
                        value=data_inputs['email']
                    )
                ],size=6),

                Col([
                    dmc.Select(
                        label="Rol",
                        placeholder="Select",
                        value=data_inputs['rol'],
                        data= roles_,
                        id = "rol",
                        clearable=False
                    ),
                ],size=6),
                Col([
                    dcc.Upload(dmc.Avatar(
                        
                        src=decoding_avatar(imagen_avatar,200,200) if imagen_avatar !="" and imagen_avatar != None  else None,
                        size="lg",
                        radius="xl",
                        mt=10,
                        id = "avatar"
                    ),id='upload-image'),
                ],size = 1),
                Col([
                    dmc.Text(id ="output-image-upload",weight=500, children=["Inserte imagen"],align="left",mt=20)
                ],size = 5),
                Col([
                    dmc.Checkbox(id="estado-user", label="Usuario Activo", mt=20,checked=data_inputs['is_active']),
                ],size=12),
                Col([
                    dmc.Button("Guardar",fullWidth=True,id="btn-save")
                ],size=6),
                Col([
                    dcc.Link(dmc.Button(id = "btn-cancel",children="Cancelar",leftIcon=DashIconify(icon="fluent:backspace-20-filled"),fullWidth=True,color="red"), href="/user/usuarios", refresh=True),
                    
                ],size=6),
                Col([
                    html.Div(id="alert")
                ]),

            ])
        ],fluid=False)
        app.clientside_callback(
        """
        function(checked) {
                if (checked) {
                    return {"colorScheme": "light"};
                } else {
                    return {"colorScheme": "dark"};
                }
        }
        """,
        Output('themeHolder','theme'),Input('themeSwitch','checked'))

        app.clientside_callback(
            """
            function(content, name) {
                if (content) {
                    return name;
                } else {
                    return "Inserte imagen";
                }
            }
            """,
            Output('output-image-upload', 'children'),
            Input('upload-image', 'contents'),
            State('upload-image', 'filename')
        )    
        
        app.clientside_callback(
            """
            function validate_email(email) {
                if (email.includes("@") || email === "") {
                    return false;
                } else {
                    return "Incorrecto";
                }
            }
            """,
            Output('email', 'error'),
            [Input('email', 'value')]
        )
        #upload-imagem, avatar
        app.clientside_callback(
            """
            function(content) {
                const image = content.split(',')[1];
                if (content) {
                    return 'data:image/png;base64,' + image;
                }
            }
            """,
            Output("avatar", "src"),
            Input("upload-image", "contents")
        )
        @app.callback(Output('modal-alert', 'opened'),
                    Output('modal-alert', 'children'),
                    Output("modal-alert","withCloseButton"),
                    Input('btn-save', 'n_clicks',),#0
                    State('name', 'value'),#1
                    State('last_name', 'value'),#2
                    State('phone', 'value'),#3
                    State('email', 'value'),#4
                    State('rol', 'value'),#5
                    State('upload-image', 'contents'),#6
                    State("estado-user","checked"),#7
                    State("modal-alert", "opened"),#8
                    prevent_initial_call=True,
        )
        def update_output(*args):
            n_clicks =args[0]
            
            if n_clicks:
                name_ = args[1]
                last_name_ = args[2]
                phone_ = args[3]
                email = args[4]
                rol = args[5]
                img = args[6]
                check = args[7]
                modal = args[8]
                if (name_ !="" or name_ != None ):
                    #print(check,rol)
                    #try :
                        #rint((data_inputs["id"],name_,last_name_,phone_,email,rol,check))
                        updateProfile(data = (data_inputs["id"],name_,last_name_,phone_,email,rol,img,check))
                        #return not modal, modal_success,True
                    #except:
                        return not modal, modal_success, True
                    
                    #if args[-2] == False and args[6] == args[7] and args[4].__contains__("@") == True and  (args[5] !="" or args[5] != None ) and validar_contraseña(args[6]) == True and (args[3] !="" or args[3] != None ):#
                        #createProfile(data=args[1:-2])
                        #return not args[13], modal_success,False#dmc.Alert("AW", title="Success!", color="green")
                    #else:
                    #    return not args[13], modal_error,False#dmc.Alert("error!", title="Danger!", color="red")
                else:
                    return not modal, modal_error, True   

       

        
        return app
        
        


