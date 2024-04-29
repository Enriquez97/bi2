from ..models import KPI
from ...handler_data.models import StoreProcedure
def createKPI(dict_kpi: dict):
    kpi_register = KPI(
                    sp = StoreProcedure.objects.get(sp_name = dict_kpi["sp_name"]),
                    name = dict_kpi["kpi_name"],
                    type = dict_kpi["type_graph"],
                    operation = dict_kpi["operation"],
                    variable_categorical = dict_kpi["var_cate"],
                    variable_numerical = dict_kpi["var_num"],
                    figure = dict_kpi["figure"],
                )
    return kpi_register.save()