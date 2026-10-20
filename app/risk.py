"""Cálculo determinista. La IA nunca calcula ni acepta el riesgo."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
TREE = json.loads((DATA / 'ssvc/deployer.json').read_text())
OUTCOMES = {'D': 'Defer', 'S': 'Scheduled', 'O': 'Out-of-Cycle', 'I': 'Immediate'}
INPUTS = {'exploitation': 'ssvc:E:1.1.0', 'exposure': 'ssvc:EXP:1.0.1',
          'automatable': 'ssvc:A:2.0.0', 'human_impact': 'ssvc:HI:2.0.2'}


def ordinal(value):
    if type(value) is not int or not 1 <= value <= 5:
        raise ValueError('Cada nivel debe ser un entero entre 1 y 5.')
    return value


def score(likelihood, impacts):
    ordinal(likelihood)
    if set(impacts) != {'operation', 'people', 'data', 'financial'}:
        raise ValueError('Se requieren cuatro dimensiones de impacto.')
    impact = max(ordinal(v) for v in impacts.values())
    return {'likelihood': likelihood, 'impact': impact, 'index': 4 * likelihood * impact,
            'formula': '4 × L × max(operación, personas, datos, finanzas)',
            'meaning': 'Índice ordinal docente; no es porcentaje de probabilidad ni pérdida esperada.'}


def ssvc(values):
    if set(values) != set(INPUTS):
        raise ValueError('Faltan entradas de SSVC Deployer.')
    for key, field in INPUTS.items():
        allowed = {v['key'] for v in TREE['decision_points'][field]['values']}
        if values[key] not in allowed:
            raise ValueError(f'Entrada SSVC inválida: {key}')
    for row in TREE['mapping']:
        if all(row[field] == values[key] for key, field in INPUTS.items()):
            return {'tree': 'ssvc:DT_DP:1.0.0', 'outcome': OUTCOMES[row[TREE['outcome']]],
                    'inputs': values, 'source': 'CERT/CC, tabla oficial vendorizada sin modificar'}
    raise ValueError('La combinación no está en la tabla oficial.')


def evaluate(payload):
    return {**score(payload['likelihood'], payload['impacts']), 'ssvc': ssvc(payload['ssvc'])}
