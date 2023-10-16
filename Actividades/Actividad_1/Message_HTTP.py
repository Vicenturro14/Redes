from constants import *

class Message_HTTP:
    """
    Clase que representa un mensaje HTTP.
    """
    def __init__(self, head_dict : dict, body : str) -> None:
        self.head = head_dict
        self.body = body

    def __str__(self) -> str:
        """ Retorna la representación en string del mensaje HTTP. """
        
        # Se agrega primero la start line del head
        msg_str = self.head["start line"] + HEAD_ENDLINE

        # Luego se agragan el resto de headers
        for name, content in self.head.items():
            header = name + ": " + content
            msg_str += header + HEAD_ENDLINE
        
        # Se agrega un nuevo salto de línea para marcar el final del head
        msg_str += HEAD_ENDLINE

        # Se agrega el body
        msg_str += self.body

        return msg_str
    
    def add_header(self, header_name : str, header_content : str):
        """
        Agrega un header al head del mensaje HTTP.
        Si el header ya existe, cambia su contenido.
        """
        
        self.head[header_name] = header_content

    def get_request_destiny_address(self):
        """ Retorna la dirección de destino del mensaje HTTP obtenida desde el header Host.
        Se asume que el método solo será utilizado cuando el mensaje sea una request y no una response. """

        return self.head["Host"]
    
    def get_URI(self):
        """ Retorna la URI de destino del mensaje HTTP"""

        start_line_list = self.head["start line"].split(" ")
        return start_line_list[1]
    
    def replace_forbidden_words(self, forbidden_words_list : list):
        
        for forbidden_word_dict  in forbidden_words_list:
            for forbidden_word, replacement in forbidden_word_dict.items():
                self.body = self.body.replace(forbidden_word, replacement)
        self.head["Content-Length"] = str(len(self.body.encode()))
        
