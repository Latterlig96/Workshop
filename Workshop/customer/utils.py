from typing import Dict


def create_username_from_email(cleaned_data: Dict) -> str:
    return cleaned_data["email"].split("@")[0]
