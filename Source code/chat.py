import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
def chat(query):
    try: 
        cred = credential.Credential("AKIDD2d1CHbsLh8MTKwEQSJvJPFqDUbTd1jF", "Yu7A0BEAxbAd7g4IIJsNiusjuFpFTUt5") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

        req = models.ChatBotRequest()
        params = {
            "Query": query
        }
        req.from_json_string(json.dumps(params))

        resp = client.ChatBot(req)
        res = eval(resp.to_json_string())
        print(res["Reply"])
        return res["Reply"]

    except TencentCloudSDKException as err: 
        print(err) 
