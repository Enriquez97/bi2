from ..models import Dashboard

def createDashboard(name = "", dict_layout = {}, type = ""):
    dashboard_register = Dashboard(
                            name = name,
                            dashboard_layout = dict_layout,
                            type_dashboard = type
                        )
    return dashboard_register.save()