from .base_command import BaseCommand
import os
import torch
import soundfile as sf

import paimon.utils
import paimon.commons
from paimon.models import SynthesizerTrn
from paimon.text.symbols import symbols
from paimon.text import text_to_sequence


class VITSCommand(BaseCommand):
    '''派蒙语音vits'''

    def __init__(self) -> None:
        self.VOICE_FILE_PATH = '/save/vits/'
        self.MODELS_FILE_PATH = '/save/vits/models/'
        self.MODEL_FILE_NAME = 'G_1434000.pth'
        os.makedirs(self.VOICE_FILE_PATH, exist_ok=True)
        os.makedirs(self.MODELS_FILE_PATH, exist_ok=True)
        self.hps = paimon.utils.get_hparams_from_file("paimon/biaobei_base.json")
        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            **self.hps.model).cpu()
        _ = self.net_g.eval()
        _ = paimon.utils.load_checkpoint(
            self.MODELS_FILE_PATH + self.MODEL_FILE_NAME, self.net_g, None)
        super().__init__()

    def get_text(self, text, hps):
        text_norm = text_to_sequence(text, hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = paimon.commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm).cpu()
        return text_norm

    def getCommandName(self):
        return '/vits'

    def execute(self, user=None, params=None, is_group=False):
        if len(params) > 1:
            text = params[1:]
            length_scale = 1.0
            filename = 'paimon'
            audio_path = f'{self.VOICE_FILE_PATH}{filename}.wav'
            stn_tst = self.get_text(text, self.hps)
            with torch.no_grad():
                x_tst = stn_tst.cpu().unsqueeze(0)
                x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cpu()
                audio = self.net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8,
                                         length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()
            sf.write(audio_path, audio, samplerate=self.hps.data.sampling_rate)
            return f'@fil@{audio_path}'
        else:
            return 'param need text';
