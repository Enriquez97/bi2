from ..models import StoreProcedure, DataConfig


def createDataConfig(config_data : dict, sp_name : str):
    data_config = DataConfig(config_sp_name =f"data-config-{sp_name}",config = config_data, )
    data_config.save()
    sp_config_update = StoreProcedure.objects.filter(sp_name = sp_name)
    return sp_config_update.update(config = data_config)