import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tbp.v20190627 import tbp_client, models

def get_response(question):
    try: 
        cred = credential.Credential("AKIDD2d1CHbsLh8MTKwEQSJvJPFqDUbTd1jF", \
                                     "Yu7A0BEAxbAd7g4IIJsNiusjuFpFTUt5")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tbp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tbp_client.TbpClient(cred, "", clientProfile) 

        req = models.TextProcessRequest()
        params = {
            "BotId": "1e821b18-dd0a-4ec1-90d1-e4258a4dcbb7",
            "BotEnv": "release",
            "InputText": question,
            "TerminalId": "None"
        }
        req.from_json_string(json.dumps(params))

        resp = client.TextProcess(req)
        res = eval(resp.to_json_string())
        print(res['ResponseMessage']['GroupList'][0]['Content'])
        return res['ResponseMessage']['GroupList'][0]['Content']

    except TencentCloudSDKException as err: 
        print(err) 

