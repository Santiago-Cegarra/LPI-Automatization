from playwright.sync_api import sync_playwright


def _create_profile(path: str):
    with sync_playwright() as p:
        user_data_dir = path
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir
        )
        browser.close()
        print(f"Perfil creado exitosamente en: {path}\n")
