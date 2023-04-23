import base64
import hashlib
import hmac
import time
import json
import requests


class APIException(Exception):
    """Exception class to handle general API Exceptions
        `code` values
        `message` format
    """
    def __init__(self, response):
        self.code = ''
        self.message = 'Unknown Error'
        try:
            json_res = response.json()
        except ValueError:
            self.message = response.content
        else:
            if 'detail' in json_res:
                self.message = json_res['detail']

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'APIException {}: {}'.format(self.code, self.message)


def compact_json_dict(data):
    """convert dict to compact json
    :return: str
    """
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)


class Client(object):
    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()
        self.API_URL = 'http://localhost:8000/back/'

    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'API-KEY': self.API_KEY}
        session.headers.update(headers)
        return session

    @staticmethod
    def _get_params_for_sig(data):
        """Convert params to ordered string for signature
        :param data:
        :return: ordered parameters like amount=10&price=1.1&type=BUY
        """
        return '&'.join(["{}={}".format(key, data[key]) for key in data])

    def _generate_signature(self, nonce, method, path, data):
        """Generate the call signature
        :param path:
        :param data:
        :param nonce:
        :return: signature string
        """
        data_json = ""
        endpoint = path
        if method == "get":
            if data:
                query_string = self._get_params_for_sig(data)
                endpoint = "{}?{}".format(path, query_string)
        elif data:
            data_json = compact_json_dict(data)
        sig_str = ("{}{}back/{}".format(nonce, method.upper(), endpoint).replace("'", '"').replace(" ", "")).encode('utf-8')

        m = hmac.new(self.API_SECRET.encode('utf-8'), sig_str, hashlib.sha256)
        return base64.b64encode(m.digest())
    

    def _create_uri(self, path):
        return '{}{}'.format(self.API_URL, path)

    def _request(self, method, path, signed, **kwargs):

        # set default requests timeout
        kwargs['timeout'] = 100
        kwargs['data'] = kwargs.get('data', {})
        kwargs['headers'] = kwargs.get('headers', {})

        uri = self._create_uri(path)

        if signed:
            # generate signature
            nonce = int(time.time() * 1000)
            kwargs['headers']['nonce'] = str(nonce)
            kwargs['headers']['API-KEY'] = self.API_KEY
            kwargs['headers']['API-SIGN'] = self._generate_signature(nonce, method, path, kwargs['data'])

        if kwargs['data'] and method == 'get':
            kwargs['params'] = kwargs['data']
            del kwargs['data']

        if signed and method != 'get' and kwargs['data']:
            kwargs['data'] = compact_json_dict(kwargs['data'])
        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)
    
    @staticmethod
    def _handle_response(response):
        if not str(response.status_code).startswith('2'):
            # print(response.json()['message'])
            raise APIException(response)
        return response.json()
            
    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request('post', path, signed, **kwargs)
    
    def _get_emb_one_sentence(self, sentence, model_id=None):
        data = {
            'sentence':sentence,
            "model_id":model_id
            
        }
        embeddings = self._post("calcemb", signed=True, data=data)
        return embeddings
    
    def _get_emb_many_sentences(self, sentences, model_id=None):
        data = {
            'sentences': sentences,
            "model_id" :model_id
        }
        embeddings = self._post("calcembm", signed=True, data=data)
        return embeddings
    
    def get_embeddings(self, input_data, model_id=None):
        if isinstance(input_data, list):
            return self._get_emb_many_sentences(input_data, model_id)
        
        if isinstance(input_data, str):
            return self._get_emb_one_sentence(input_data, model_id)  