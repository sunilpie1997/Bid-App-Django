from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from .views import *

def base_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(context["view"])
    print(response.data)
    sample={}
    # check that a ValidationError exception is raised
    if isinstance(exc, ValidationError):
    # here prepare the 'custom_error_response' and
    # set the custom response data on response object
        print(type(response.data))
        #response.data can be of list type ,so.....
        if isinstance(response.data,list):
            sample["detail"]=response.data[0]#get first message from list,example is given below:
            response.data=sample

        else:

            if response.data.get("detail",None):
                sample["detail"]=response.data["detail"][0]
                response.data=sample
            elif response.data.get("username", None):
                sample["detail"]=response.data["username"][0]
                response.data=sample
            elif response.data.get("email", None):
                sample["detail"] = response.data["email"][0]
                response.data=sample
            elif response.data.get("profile",None):
                if response.data["profile"].get("contact_no",None):
                    sample["detail"]=response.data["profile"]["contact_no"][0]
                    response.data=sample
             
        
    
    print("response",response)
    
    return response

"""
example:
{
    "error1",
    "error2",
    ......
    "errorn
}
retrieve first error as next error will be raised automatically when user corrects first one
"""