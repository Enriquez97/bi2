import uuid
import base64
from django.contrib.auth.models import User
from ...management.models import Profile,Category,Role,Company

def createProfile(data : tuple):
    name = data[0]
    surname = data[1]
    phone = data[2]
    email = data[3]
    username = data[4]
    password = data[5]
    empresa_id = Company.objects.get(id = uuid.UUID(data[7]))
    role_id = Role.objects.get(id = uuid.UUID(data[8]))
    _,imagen = data[10].split(',', 1)
    user = User.objects.create_user(username=username, email=email, password=password)
    profile = Profile(
                user = user,
                name = name,
                surname = surname,
                avatar_profile = imagen,
                phone = phone,
                company = empresa_id,
                role = role_id   
            )
    return profile.save()

def updateProfile(data : tuple):
    id = data[0]
    name = data[1]
    last_name = data[2]
    phone = data[3]
    email = data[4]
    rol = Role.objects.get(id = uuid.UUID(data[5]))

    is_active = data[7]
    
    
    
    profile = Profile.objects.get(pk = id)
    user = User.objects.get(pk =  profile.user.id)

    user.email = email
    user.is_active = is_active
    user.save()
    
    profile.name = name
    profile.surname = last_name
    
    profile.avatar_profile = data[6].split(',')[1] if data[6] != None else profile.avatar_profile
    profile.phone = phone
    profile.role = rol   

    profile.save()
    
    return "save"
    
    



def createEmpresa(data: tuple):
    ruc = data[0]
    empresa = data[1]
    telefono = data[2]
    rubro = Category.objects.get(id = uuid.UUID(data[3]))
    ip = data[4]
    token = data[5]
    server = data[6]
    bd = data[7]
    user_bd = data[8]
    password_bd = data[9]
    _,imagen = data[10].split(',', 1)
    tipo_conexion = data[11]
    
    empresa = Company(
        ruc = ruc,
        description = empresa,
        phone = telefono,
        avatar_profile = imagen,
        ip = ip,
        token = token,
        
        server = server,
        database = bd,
        uid = user_bd,
        uid_pass = password_bd,
        type_con = tipo_conexion,
        
        category = rubro
    )
    return empresa.save()
    