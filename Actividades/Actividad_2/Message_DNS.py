class Message_DNS:
    """ Clase que representa mensajes DNS. """
    def __init__(self, header_dict : dict, qname : str, answer : list, auth : list, add : list) -> None:
        self.header = header_dict
        self.qname = qname
        self.answer = answer
        self.authority = auth
        self.additional = add

    def print_dns(self) -> None:
        """ Imprime el mensaje DNS """
        print(">>--------------- HEADER SECTION ---------------<<\n")
        print("-> number_of_answer_elements = {}".format(self.header["ANCOUNT"]))
        print("-> number_of_authority_elements = {}".format(self.header["NSCOUNT"]))
        print("-> number_of_additional_elements = {}".format(self.header["ARCOUNT"]))
        print(">>----------------------------------------------<<\n")


        print(">>---------------- QUERY SECTION ---------------<<\n")
        print("-> domain_name_in_query = {}".format(self.qname))
        print(">>----------------------------------------------<<\n")


        print(">>---------------- ANSWER SECTION --------------<<\n")
        if self.header["ANCOUNT"] > 0:
            print("-> all_resource_records = {}".format(self.answer))

            first_answer = self.answer[0]
            print("-> first_answer = {}".format(first_answer))
            print("-> domain_name_in_answer = {}".format(first_answer["NAME"]))
            print("-> answer_class = {}".format(first_answer["RCLASS"]))
            print("-> answer_type = {}".format(first_answer["RTYPE"]))
            print("-> answer_rdata = {}".format(first_answer["RDATA"]))
            print("-> answer_time_to_live = {}".format(first_answer["TTL"]))
        else:
            print("-> number_of_answer_elements = 0")
        print(">>----------------------------------------------<<\n")


        print(">>-------------- AUTHORITY SECTION -------------<<\n")
        # authority section
        if self.header["NSCOUNT"] > 0:
            print("-> authority_section_list = {}".format(self.authority))

            if len(self.authority) > 0:
                authority_section_RR_0 = self.authority[0] 
                print("-> authority_section_RR_0 = {}".format(authority_section_RR_0))
                print("-> auth_type = {}".format(authority_section_RR_0["RTYPE"]))
                print("-> auth_class = {}".format(authority_section_RR_0["RCLASS"]))
                print("-> auth_time_to_live = {}".format(authority_section_RR_0["TTL"]))
                print("-> authority_section_0_rdata = {}".format(authority_section_RR_0["RDATA"]))
                if authority_section_RR_0["RTYPE"] == "NS":
                    print("-> name_server_domain = {}".format(authority_section_RR_0["NAME"]))
        else:
            print("-> number_of_authority_elements = 0")
        print(">>----------------------------------------------<<\n")


        print(">>------------- ADDITIONAL SECTION -------------<<\n")
        if self.header["ARCOUNT"] > 0:
            print("-> additional_records = {}".format(self.additional))

            first_additional_record = self.additional[0]
            print("-> first_additional_record = {}".format(first_additional_record))
            print("-> ar_class = {}".format(first_additional_record["RCLASS"]))
            print("-> ar_type = {}".format(first_additional_record["RTYPE"]))
            print("-> ar_time_to_live = {}".format(first_additional_record["TTL"]))
            
            if first_additional_record["RTYPE"] == 'A':
                print("-> first_additional_record_rname = {}".format(first_additional_record["NAME"]))
                print("-> first_additional_record_rdata = {}".format(first_additional_record["RDATA"]))
        else:
            print("-> number_of_additional_elements = 0")
        print(">>----------------------------------------------<<\n\n\n")

    def has_type_A_answer(self) -> bool:
        if self.header["ANCOUNT"] > 0:
            for answer in self.answer:
                if answer["RTYPE"] == 'A':
                    return True
        return False
    
    def first_type_NS_auth(self) -> dict:
        if self.header["NSCOUNT"] > 0:
            for auth in self.authority:
                if auth["RTYPE"] == "NS":
                    return auth
        return None
    
    def first_type_A_add(self) -> dict:
        if self.header["ARCOUNT"] > 0:
            for add in self.additional:
                if add["RTYPE"] == 'A':
                    return add
        return None
    
    def get_resolved_answer(self) -> str:
        if self.header["ANCOUNT"] > 0:
            for answer in self.answer:
                if answer["RTYPE"] == 'A':
                    return answer
        return None