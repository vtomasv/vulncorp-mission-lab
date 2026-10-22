"""Station bridge: fixed catalog, authenticated controller, signed station receipt."""
import json
from .continuation import COMMANDS
from .secure import secret

def execute(action,agent):
    code,body=agent.http('http://mission:8000/api/continuation/action',{'action':action},
                         {'X-Station-Key':secret('appdesk')},timeout=280)
    if code!=200:raise ValueError(body.get('error','No se completó la acción.'))
    filename=action+'.json'
    saved=body.get('bundle',body)
    path=agent.write_student(filename,saved)
    result={'campaign':body['campaign'],'episode':body['episode'],'event_ids':[r['id'] for r in body['events']],'file':path}
    return result,json.dumps(body,ensure_ascii=False,indent=2)+'\nArchivo: '+path+'\nVuelve a la misión y contrasta lo observado antes de conservar tu decisión.'
