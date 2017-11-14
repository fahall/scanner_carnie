import scannerpy
from scannerpy.stdlib import parsers, pykernel


class CarnieKernel:

    def execute(self, frame, bboxes):
        rc = RudeCarnie(model_dir='/n/scanner/models/rude-carnie')
        bboxes = parsers.deserialize(bboxes)
        for bb in bboxes:
            face_img = frame[int(h * bb.y1):int(h * bb.y2),
                             int(w * bb.x1):int(w * bb.x2)]
            face_img = cv2.resize(face_img, (out_size, out_size))
            face_img = facenet.prewhiten(face_img)
            gender = rc.get_gender(faces, single_look=True)

        return [result]


KERNEL = CarnieKernel
