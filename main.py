import os.path as osp
import os
from dotenv import load_dotenv
load_dotenv()

from neuralogic.Settings import Settings
from neuralogic.Sources import Sources, LearningMode
from neuralogic.Pipeline import Pipeline
from neuralogic import initialize


import neuralogic.PytorchLayer as torchlayer


def train(neuralogic_path, pytorch_path):
    initialize(os.environ["CLASSPATH"])

    settings = Settings()
    template = """
        {3,1} atom_embed(A) :- c_26(A).
        {3,1} atom_embed(A) :- c_27(A).
        {3,1} atom_embed(A) :- c_25(A).
        {3,1} atom_embed(A) :- c_28(A).
        {3,1} atom_embed(A) :- c_29(A).
        {3,1} atom_embed(A) :- o_49(A).
        {3,1} atom_embed(A) :- br_94(A).
        {3,1} atom_embed(A) :- o_42(A).
        {3,1} atom_embed(A) :- o_45(A).
        {3,1} atom_embed(A) :- o_41(A).
        {3,1} atom_embed(A) :- o_40(A).
        {3,1} atom_embed(A) :- i_95(A).
        {3,1} atom_embed(A) :- f_92(A).
        {3,1} atom_embed(A) :- h_1(A).
        {3,1} atom_embed(A) :- h_3(A).
        {3,1} atom_embed(A) :- c_10(A).
        {3,1} atom_embed(A) :- c_14(A).
        {3,1} atom_embed(A) :- c_194(A).
        {3,1} atom_embed(A) :- c_195(A).
        {3,1} atom_embed(A) :- c_16(A).
        {3,1} atom_embed(A) :- h_8(A).
        {3,1} atom_embed(A) :- c_19(A).
        {3,1} atom_embed(A) :- c_230(A).
        {3,1} atom_embed(A) :- c_232(A).
        {3,1} atom_embed(A) :- o_50(A).
        {3,1} atom_embed(A) :- n_36(A).
        {3,1} atom_embed(A) :- o_52(A).
        {3,1} atom_embed(A) :- n_35(A).
        {3,1} atom_embed(A) :- n_34(A).
        {3,1} atom_embed(A) :- o_51(A).
        {3,1} atom_embed(A) :- n_32(A).
        {3,1} atom_embed(A) :- n_31(A).
        {3,1} atom_embed(A) :- cl_93(A).
        {3,1} atom_embed(A) :- c_21(A).
        {3,1} atom_embed(A) :- c_22(A).
        {3,1} atom_embed(A) :- n_38(A).
        atom_embed/1 {3,1}
        {3,1} bond_embed(B) :- b_1(B).
        {3,1} bond_embed(B) :- b_2(B).
        {3,1} bond_embed(B) :- b_3(B).
        {3,1} bond_embed(B) :- b_4(B).
        {3,1} bond_embed(B) :- b_5(B).
        {3,1} bond_embed(B) :- b_7(B).
        bond_embed/1 {3,1}
    
        l1_embed(X) :- {3,3} atom_embed(X), {3,3} atom_embed(Y), bond(X,Y,B), bond_embed(B).
        l2_embed(X) :- {3,3} l1_embed(X), {3,3} l1_embed(Y), bond(X,Y,B), bond_embed(B).
        l3_embed(X) :- {3,3} l2_embed(X), {3,3} l2_embed(Y), bond(X,Y,B), bond_embed(B).
        
        {1,3} predict :- l3_embed(X).
    """

    sources = Sources.from_str(template, settings, LearningMode.TRAIN_ONLY)

    pipeline = Pipeline(settings, sources)
    r, s = pipeline.execute(sources)

    dataset = torchlayer.PytorchDataset(pytorch_path)
    device = torchlayer.get_device()
    model = torchlayer.get_model(dataset, device)
    optimizer = torchlayer.get_optimizer(model)

    torchlayer.eval(dataset, model, optimizer, device)


train("./dataset/molecules/mutagenesis", osp.join(osp.dirname(osp.realpath(__file__)), "..", "dataset", "pytorch_mutagenesis"))
