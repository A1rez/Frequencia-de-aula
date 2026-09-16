import os
import shutil


def inicializar_banco(page):
    destino = os.path.join(page.app_storage_path, "frequencia.db")

    # já existe?
    if os.path.exists(destino):
        return destino

    # banco original do projeto
    origem = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "frequencia.db",
    )

    shutil.copy2(origem, destino)

    return destino