import argostranslate.package


def intall_model_tranlate():
    from_code = "en"
    to_code = "es"

    argostranslate.package.update_package_index()

    packages = argostranslate.package.get_available_packages()

    package = next(
        p for p in packages if p.from_code == from_code and p.to_code == to_code
    )

    argostranslate.package.install_from_path(package.download())

    print("Modelo inglés → español instalado")
