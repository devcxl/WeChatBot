
import torch
import soundfile as sf

import utils
import commons
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

print(torch.cuda.is_available())
print(torch.version.cuda)

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm).cpu()
    return text_norm


hps = utils.get_hparams_from_file("config.json")

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).cpu()
_ = net_g.eval()

_ = utils.load_checkpoint(
    '/home/devcxl/IdeaProjects/VITS-Paimon/models_all/G_1434000.pth', net_g, None)


text = "失忆症的原因究竟是什么呢？关于这个世界最初的美好记忆，能否被寻回呢？"
length_scale = 1.0
filename = 'test1'
audio_path = f'{filename}.wav'
stn_tst = get_text(text, hps)
with torch.no_grad():
    x_tst = stn_tst.cpu().unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cpu()
    audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8,
                        length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()
sf.write(audio_path, audio, samplerate=hps.data.sampling_rate)
