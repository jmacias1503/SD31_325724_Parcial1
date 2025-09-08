PAYLOAD_BUFFER_SIZE_BYTES = 24
def is_valid_ip_address(ip_address: str) -> bool:
    values = ip_address.split('.')
    if len(values) != 4:
        return False
    for i in values:
        try:
            if int(i) not in range(256):
                return False
        except ValueError:
            return False
    return True
class Student:
    def __init__(self, name: str, password: str, gender: str, age: int, email: str, major: str):
        self.__name = name
        self.__password = password
        self.__gender = gender
        self.__age = age
        self.__email = email
        self.__major = major
    def get_name() -> str:
        return self.__name
    def set_name(new_name: str):
        self.__name = new_name
    def get_password() -> str:
        return self.__password
    def set_password(new_password: str):
        self.__password = new_password
    def get_gender() -> str:
        return self.__gender
    def set_gender(new_gender: str):
        self.__gender = new_gender
    def get_age() -> int:
        return self.age
    def set_age(new_age: int):
        self.__age = new_age
    def get_email() -> str:
        return self.__email
    def set_email(new_email: str):
        self.__email = new_email
    def get_major() -> str:
        return self.__major
    def set_major(new_major):
        self.__major = new_major
