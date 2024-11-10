from prompts import Prompts
from chat import Chat

class Summarizer:
    def __init__(self,
                chat:Chat,
                ):
        self.chat = chat
    
    def summarize_email_product(self, documents:dict,):
        # retrive the necessary prompts
        sys_msg = Prompts.Summarize.SYSTEM_MESSAGE
        guard_rails = Prompts.Summarize.GUARD_RAILS

        # create the message content
        message = ""
        for title, content in documents.items():
            cur_msg = f"title : {title}\n\n"
            cur_msg += f"content : {content}\n\n"
            message += cur_msg

        message += guard_rails

        # pass it through the chat
        output = self.chat.chat(system_msg=sys_msg,
                                user_msgs=[message])
        
        return output
    
    def summarize_qa_lead(self, qa:tuple[str, str], lead_info: str):
        # retrive the necessary prompts
        sys_msg = Prompts.Summarize.QA_SYSTEM_MSG
        guard_rails = Prompts.Summarize.GUARD_RAILS

        # create the message content
        message = "Lead Info : " + lead_info + "\n\n"
        
        for question, response in qa:
            if response == Prompts.QA.DEFAULT_RESPONSE:
                continue
            message += "Question Asked by Lead : " + question + "\nAI Generated Response : " + response + "\n\n"

        message += guard_rails

        # pass it through the chat
        output = self.chat.chat(system_msg=sys_msg,
                                user_msgs=[message])
        
        return output

