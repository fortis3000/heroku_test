from flask import Flask
from flask import request
import requests
from flask import make_response
import os
import json
import traceback
from xml.etree import ElementTree as ET
import string
import random


#import self libs
import test.test_get_message as t_gm
from models import main as models_main
from number import number_calc

import logging
import timber

logging.basicConfig(level=logging.DEBUG)
log_apikey = os.getenv('timber_apikey')
logger = logging.getLogger(__name__)

timber_handler = timber.TimberHandler(source_id='14767', api_key=log_apikey)
timber_handler.setLevel(logging.DEBUG) # set level for EACH handler
logger.addHandler(timber_handler)


application = Flask(__name__)  # Change assignment here


#define loger func
def log(logger, json_params=None,step='new',internal_id=None):
    logger.info("Logs: step: {0}, params: {1}".format(step, json.dumps(json_params)))


#create random string
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#test
@application.route("/")  
def hello():
    resp = "Hello World!"
    return resp


#get message from messanger and calc messages models
@application.route('/get_message', methods=['GET', 'POST'])  
def get_message():
    internal_id = randomString(10)
    status_code = 200
    
    response = {'status' : 'ok',
                'code' : 200,
                'message_id' : None,
                'dialog_id' : None,
                'participants_id' : None,
                'user_id' : None,
                'models' :[]
               }
    try:
        log(logger,step='new',internal_id=internal_id)
        getData = request.get_data()
        json_params = json.loads(getData)
        log(logger,json_params,'get json_params',internal_id)

        # json_params = {'message_id':0,
        #                'dialog_id':0,
        #                'participants_id':0,
        #                'user_id':0,
        #                'content':'test content',
        #                'created_at':111111111,
        #            }


        status_code = 400
        response['message_id'] = json_params['message_id']
        response['dialog_id'] = json_params['dialog_id']
        response['participants_id'] = json_params['participants_id']
        response['user_id'] = json_params['user_id']


        #make test models predict (for message , model_id = 0)
        #model_resp = t_gm.make_random_model(json_params = json_params , model_id = 0, model_to = 'message_id')
        #response['models'].append(model_resp)
        
        #make real emoji predict for message
        status_code = 500
        response['models'] = models_main.main(json_params = json_params , model_to = 'message_id')
        log(logger,json_params,'model done',internal_id)
        
        status_code = 200
        
        
    except:
        if status_code == 200:
            status_code = 500
        traceback.print_exc()
        response['status'] = 'error'
        response['code'] = 501
        log(logger,json_params,'some error',internal_id)


    response = json.dumps(response)
    # print(response)
    return str(response)  , status_code

# get number and multiplying
@application.route('/sadiakhmatov_best', methods=['GET', 'POST'])
def get_mult():
    internal_id = randomString(10)
    status_code = 200

    response = {'number': None}

    try:
        log(logger, json_params=None, step='New', internal_id=internal_id)
        getData = request.get_data()
        json_params = json.loads(getData)
        log(logger, json_params=json_params, step='get json number', internal_id=internal_id)

        # local
        # json_params = {'number': '123'}


        response['number'] = number_calc(json_params['number'])
        log(logger, json_params=response, step='mult done', internal_id=internal_id)

        status_code = 200


    except:
        if status_code == 200:
            status_code = 500
        traceback.print_exc()
        response['status'] = 'error'
        response['code'] = 501
        log(logger, json_params=response, step='some error', internal_id=internal_id)

    response = json.dumps(response)
    # print(response)
    return str(response), status_code

if __name__ == "__main__":
    #heroku
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0' , threaded=True)
    #local
    #application.run()