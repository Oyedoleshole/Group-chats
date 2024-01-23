from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time

def get_token(request):
    random_number = random.randint(1,230)
    appId = '20f638f7c0a34553b60f309b32a396f0'
    appCertificate = '33af446302424505b641e241ccc9e5ce'
    channelName = request.GET.get('channel')
    uid = random_number
    print("The UID is generated=====>",uid)
    role = 1
    expirationTimeInSec = 3600 * 24
    currentTime = time.time()
    privilegeExpiredTs = currentTime + expirationTimeInSec
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid}, safe=False)