from groq import Groq
import streamlit as st

class Chat:
    def __init__(self,
                api_key_path = "./api_key",
                model="llama3-8b-8192", 
                temperature=0,
                max_tokens=2048,
                top_p=1,
                stop=None,
                stream=False,
                ):
        # groq parameters
        self.api_key_path = api_key_path
        self.model = model

        # model parameters
        self.__temperature = temperature
        self.__max_tokens = max_tokens
        self.__top_p = top_p
        self.__stop = stop
        self.__stream = stream

        # read api key
        self.read_api_key()

    def read_api_key(self):
        # try:
        #     with open(self.api_key_path, "r") as f:
        #         api_key = f.readline()
        # except:
        api_key = st.secrets["groq_api_key"]
        self.client = Groq(api_key=api_key)

    def __construct_messages__(self, user_msgs, system_msg=None, assistant_msgs=None):
        messages = []

        if system_msg:
            msg = {
                "role" : "system",
                "content" : system_msg
            }
            messages.append(msg)

        while user_msgs:
            cur_user_msg = user_msgs.pop(0)
            user_msg = {
                "role" : "user",
                "content" : cur_user_msg
            }
            messages.append(user_msg)

            if assistant_msgs:
                cur_assisant_msg = assistant_msgs.pop(0)
                assistant_msg = {
                    "role" : "assistant",
                    "content" : cur_assisant_msg
                }
                messages.append(assistant_msg)

        return messages
            

    def chat(self, 
            user_msgs:list[str], 
            system_msg:str = None, 
            assistant_msgs:list[str] = None,
            _temperature:float=None,
            _max_tokens:int=None,
            _top_p:float=None,
            _stop:str=None,
            _stream:bool=None):
        
        # set defaults
        _temperatue = _temperature if _temperature is not None else self.__temperature
        _max_tokens = _max_tokens if _max_tokens is not None else self.__max_tokens
        _top_p = _top_p if _top_p is not None else self.__top_p
        _stop = _stop if _stop is not None else self.__stop
        _stream = _stream if _stream is not None else self.__stream

        # construct the messages
        messages = self.__construct_messages__(user_msgs=user_msgs, system_msg=system_msg, assistant_msgs=assistant_msgs)
        
        # get the chat completion
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=_temperatue,
            max_tokens=_max_tokens,
            top_p=_top_p,
            stop=_stop,
            stream=_stream
        )

        # retrive the outputs
        __reason_for_stop__ = chat_completion.choices[0].finish_reason
        output = chat_completion.choices[0].message.content

        # handle exceptions
        if __reason_for_stop__ != "stop":
            print("[COLCA-WARNING] The chat is stopped because of token limit exceeded : ", __reason_for_stop__)

        return output
    
if __name__ == "__main__":
    c = Chat()
    c.chat(["hi, how are you?"])
