from rolepermissions.roles import AbstractUserRole


class Nit10(AbstractUserRole):
    available_permissions = {'tudo': True}


class Clientes(AbstractUserRole):
    available_permissions = {'consultar_os': True}

class Abastecimentos(AbstractUserRole):
    available_permissions = {'abastecer': True}