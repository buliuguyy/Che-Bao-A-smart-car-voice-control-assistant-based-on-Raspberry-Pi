import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models


def translation(content, source="zh", target="en"):
    try: 
        cred = credential.Credential("AKIDD2d1CHbsLh8MTKwEQSJvJPFqDUbTd1jF", "Yu7A0BEAxbAd7g4IIJsNiusjuFpFTUt5") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile) 

        req = models.TextTranslateRequest()
        params = {
        "SourceText": content,
        "Source": source,
        "Target": target,
        "ProjectId": 0
        }
        req.from_json_string(json.dumps(params))

        resp = client.TextTranslate(req) 
        res = eval(resp.to_json_string())
        return res["TargetText"]

    except TencentCloudSDKException as err: 
        print(err) 
