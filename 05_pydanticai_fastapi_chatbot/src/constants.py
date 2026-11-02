"""Modeller som används i chatboten, samlade på ett ställe.

Byt modell här så slår det igenom överallt där konstanten används.
"""

from model import nvidia_model

# Liten och snabb modell, räcker för enkla skämt
MODEL_SMALL = nvidia_model("nvidia/nemotron-3.5-lightning-30b-a3b")

# Större modell, bättre svar men långsammare
MODEL_MEDIUM = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")