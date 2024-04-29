import pandas as pd
import numpy as np
import uuid
from ...resource.utils.data import decoding_avatar

def user_loggedin(profile_user: dict):
    values_login = {}
    values_login["name_user"] = profile_user.name +" "+ profile_user.surname
    values_login["avatar_profile"] = decoding_avatar(profile_user.avatar_profile,200,200)
    values_login["avatar_company"] = decoding_avatar(profile_user.company.avatar_profile,115,40)
    return values_login
    