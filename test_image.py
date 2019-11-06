import cv2
from PIL import Image
import argparse
from pathlib import Path
from multiprocessing import Process, Pipe, Value, Array
import torch
from config import get_config
from mtcnn import MTCNN
from Learner import face_learner
from utils import load_facebank, draw_box_name, prepare_facebank
import numpy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='for face verification')
    parser.add_argument("-s", "--save", help="whether save", action="store_true")
    parser.add_argument('-th', '--threshold', help='threshold to decide identical faces', default=1.54, type=float)
    parser.add_argument("-u", "--update", help="whether perform update the facebank", action="store_true")
    parser.add_argument("-tta", "--tta", help="whether test time augmentation", action="store_true")
    parser.add_argument("-c", "--score", help="whether show the confidence score", action="store_true")
    args = parser.parse_args()

    conf = get_config(False)

    mtcnn = MTCNN()
    print('mtcnn loaded')

    learner = face_learner(conf, True)
    learner.threshold = args.threshold
    if conf.device.type == 'cpu':
        learner.load_state(conf, 'cpu_final.pth', True, True)
    else:
        learner.load_state(conf, 'final.pth', True, True)
    learner.model.eval()
    print('learner loaded')
    print(learner.model)
    input("MODEL")

    if True:
        targets, names = prepare_facebank(conf, learner.model, mtcnn, tta=args.tta)
        print('facebank updated')
    else:
        targets, names = load_facebank(conf)
        print('facebank loaded')

    # inital camera

    #image_cv=imag("/media/velab/dati/faces_emore/test/test1.jpeg",cv2.COLOR_RGB2BGR)



        #                 image = Image.fromarray(frame[...,::-1]) #bgr to rgb
    #image = Image.fromarray(image_cv)
    image= Image.open("/media/velab/dati/faces_emore/test/test2.jpeg")
    #image.show()
    #input("FIRST IMAGE")
    # faces rappresenta un arra
    bboxes, faces = mtcnn.align_multi(image, conf.face_limit, conf.min_face_size)
    #faces[0].show()
    #input("IMAGE CROPPED")
    bboxes = bboxes[:, :-1]  # shape:[10,4],only keep 10 highest possibiity image
    bboxes = bboxes.astype(int)
    bboxes = bboxes + [-1, -1, 1, 1]  # personal choice
    results, score = learner.infer(conf, faces, targets, args.tta)

    print (results,score)
    input("RESULT")

    image_cv= numpy.array(image)
    image_cv = image_cv[:, :, ::-1].copy()
    for idx, bbox in enumerate(bboxes):
        if args.score:
            image_cv = draw_box_name(bbox, names[results[idx] + 1] + '_{:.2f}'.format(score[idx]), image_cv)
        else:

            image_cv = draw_box_name(bbox, names[results[idx] + 1], image_cv)


    cv2.imshow('face Capture', image_cv)
    cv2.waitKey()


