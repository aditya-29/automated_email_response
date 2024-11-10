from prompts import Prompts
from chat import Chat
from summarizer import Summarizer

class Sample:
    def __init__(self):
        with open("./sample/sample_company_information.txt", "r") as f:
            self.product_info = f.read()

        with open("./sample/sample_email_content.txt", "r") as f:
            self.email_content = f.read()

        with open("./sample/sample_lead_info.txt", "r") as f:
            self.lead_info = f.read()


class ReplyMachine:
    def __init__(self, 
                product_information: str,
                email_content: str,
                chat: Chat,
                lead_info: str,
                ):      
        self.chat = chat
        self.product_information = product_information
        self.email_content = email_content
        self.lead_info = lead_info
        self.text_summarized_email_product = None
        self.questions_asked = []
        self.qa_threads = []

    def summarize_email_and_product(self):
        # initialize a summarizer
        summarizer = Summarizer(self.chat)

        # create document dict
        documents = {}
        documents["Product Information"] = self.product_information
        documents["Email Content"] = self.email_content

        # summarize
        summarized_text = summarizer.summarize_email_product(documents=documents)
        self.text_summarized_email_product = summarized_text
        print("[INFO] Summarized Email Content and Product Information")

    def __summarize_qa_and_lead_info(self):
        # initialize the summarizer
        summarizer = Summarizer(self.chat)

        # summarize
        summarized_text = summarizer.summarize_qa_lead(qa = self.qa_threads, lead_info=self.lead_info)
        return summarized_text

        

    def __validate_question(self, question):
        # get the prompt
        message = Prompts.QA.QUESTION_JUDGE.format(question=question, context=self.product_information)

        # generate a valid/invalid for the question
        output = self.chat.chat(user_msgs=[message])

        if "valid" in output.split(" "):
            return True
        return False


    def reply(self, question):
        
        # generate product information and email summary if not generated already
        if self.text_summarized_email_product is None:
            self.summarize_email_and_product()

        # log the questions
        self.questions_asked.append(question)

        # validate the question
        validation = self.__validate_question(question)
        
        if not validation:
            print("[COLCA-ERROR] The asked question is not valid : ", question)
            self.qa_threads.append((question,Prompts.QA.DEFAULT_RESPONSE))
            return Prompts.QA.DEFAULT_RESPONSE

        # get the prompt
        message = Prompts.QA.QUESTION_REPLY.format(question=question, context=self.text_summarized_email_product)

        # generate the output from the model
        output = self.chat.chat(user_msgs=[message])

        # add it to the thread
        self.qa_threads.append((question, output))
       
        return output
    
    def quick_bytes(self):
        summaried_qa_lead = self.__summarize_qa_and_lead_info()
        return summaried_qa_lead

        

