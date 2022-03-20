from django.contrib.auth import get_user_model

class UserService:

    model = get_user_model()

    @classmethod
    def create(cls, **kwargs):
        pass

    @classmethod
    def search(cls, **kwargs):
        '''
            Criterios para sorting
            - Actividad del usuario (Grupos, Lecciones, Equipos)
            - Seguidores (si es lider)
            - Busquedas del usuario
                - Categorias
                - Tags
                - Palabras claves
            - Numero de busquedas

        '''
        pass

