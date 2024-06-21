import dash_mantine_components as dmc
from django_plotly_dash import DjangoDash
from backend.connector import APIConnector
from ...resource.helpers.make_grid import *
from ...resource.layouts.base import *
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.components.cards import card_id,card_segment,card_stack,cardGraph
from ...resource.components.notification import notification_update_show
from ...oldapp.utils import *

df = pd.read_parquet('agricola.parquet', engine='pyarrow')
df = df.drop(["NCULTIVO","POLYGON","AREA_PLANIFICADA","CODSIEMBRA","CODCAMPAÑA","SEMANA"], axis=1)
df = df[df['AÑO_CAMPAÑA']>2019]
class DashProduccion:
    #def __init__(self, ip: str, token :str):#, data_login: dict
        #self.ip = ip
        #self.token = token
    def ejecucion_campania(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        app.layout = \
        Content([
             Grid([
                 Col([dmc.Title("Ejecución de Campaña")],size=3),
                 Col([
                     dmc.MultiSelect(
                        #data=["React", "Angular", "Svelte", "Vue"],
                        id="campania",
                        label = "Campaña",
                        placeholder = "Todos",
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        #value=sorted(df['AÑO_CULTIVO'].unique()),
                        data=[{'label': i, 'value': i} for i in sorted(df['AÑO_CULTIVO'].unique())],
                        size="sm", 
                    ),
                 ],size=3),
                 
                 Col([
                    dmc.Select(
                        label="Variedad",
                        placeholder="Todos",
                        id="variedad",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size=3),
                 Col([
                     dmc.Select(
                        label="Lotes",
                        placeholder="Todos",
                        id="lote",
                        value = None,
                        data= [],
                        clearable=True
                    )
                 ],size=3),
                 
                 Col([])
                 
             ]),
        html.Div(id='notifications-update-data'),
        dcc.Store(id='data-values'),    
        ])
        @app.callback(
            Output('variedad','data'),
            Output('lote','data'),
            Output("data-values","data"),
            Output("notifications-update-data","children"),
            Input('campania','value'),
            Input('variedad','value'),
            Input('lote','value'),
        )
        def update_data(*args):
            if validar_all_none(variables = args) == True:
                dff = df.copy()
            else:
                 dff = df.query(dataframe_filtro(values= args ,columns_df=['AÑO_CULTIVO',"VARIEDAD","CONSUMIDOR"]))
            return [
                [{'label': i, 'value': i} for i in sorted(dff['VARIEDAD'].unique())],
                [{'label': i, 'value': i} for i in sorted(dff['CONSUMIDOR'].unique())],
                dff.to_dict('series'), 
                notification_update_show(text=f'Se cargaron {len(dff)} filas',title='Update')
            ]
        return app